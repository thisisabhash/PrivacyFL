import config
import datetime
import numpy as np
import pickle
import random

from client_agent import ClientAgent
from server_agent import ServerAgent
from directory import Directory
from pyspark.sql import SparkSession
from sklearn.datasets import load_digits
from sklearn.datasets import load_wine
from sklearn.datasets import load_breast_cancer
from sklearn.datasets import load_iris

from utils import data_formatting

from utils.print_config import print_config
from utils.model_evaluator import ModelEvaluator
from sklearn.preprocessing import MinMaxScaler

import csv


class Initializer:
    def __init__(self, num_clients, num_servers, iterations):
        """
        Offline stage of simulation. Initializes clients and servers for iteration as well as gives each client its data.
        :param num_clients: number of clients to be use for simulation
        :param num_servers: number of servers to be use for simulation. Personalized coding required if greater than 1.
        :param iterations: number of iterations to run simulation for
        """

        global len_per_iteration
        if config.USING_PYSPARK:
            spark = SparkSession.builder.appName('SecureFederatedLearning').getOrCreate()  # initialize spark session
            spark.sparkContext.setLogLevel("ERROR")  # supress sparks messages

#        digits = load_digits()  # using sklearn's MNIST dataset
#        X, y = digits.data, digits.target
#        temp = np.hstack((X,y))
#        np.random.shuffle(temp)
#        X = temp[:,:-1]
#        y = temp[:,-1]
        
        #iris = load_iris()
        #X, y = iris.data, iris.target
        #print('Training data size: ' + str(len(X)))
        
        reader = csv.reader(open("Skin_NonSkin.txt"), delimiter="\t")
        dataset = []
        for row in reader:
            dataset.append(row)
    
        dataset = np.array(dataset)
        np.random.shuffle(dataset)
        X = dataset[:,:-1]
        X = X.astype(np.float)
        y = dataset[:,-1]
        y = y.astype(np.int)
        
#        reader = csv.reader(open("/Users/abhash/Desktop/CS839 Data Management for ML/Project/HCV-Egy-Data.csv"), delimiter=",")
#        dataset = []
#        for row in reader:
#            dataset.append(row)
#    
#        dataset = dataset[1:]
#        dataset = np.array(dataset)
#        np.random.shuffle(dataset)
#        X = dataset[:,:-2]
#        y = dataset[:,-1]
        
        #print(X)
        #print(y)

#        scaler = MinMaxScaler()
#        scaler.fit(X)
#        X = scaler.transform(X)

        X_train, X_test = X[:-config.LEN_TEST], X[-config.LEN_TEST:]
        y_train, y_test = y[:-config.LEN_TEST], y[-config.LEN_TEST:]

        # extract only amount that we require
        number_of_samples = 0
        for client_name in config.client_names:
            len_per_iteration = config.LENS_PER_ITERATION[client_name]
            number_of_samples += len_per_iteration * iterations

        X_train = X_train[:number_of_samples]
        y_train = y_train[:number_of_samples]

        client_to_datasets = data_formatting.partition_data(X_train, y_train, config.client_names, iterations,
                                                            config.LENS_PER_ITERATION, cumulative=config.USING_CUMULATIVE, pyspark=config.USING_PYSPARK)

        #print_config(len_per_iteration=config.LEN_PER_ITERATION)
        print('\n \n \nSTARTING SIMULATION \n \n \n')

        active_clients = {'client_agent' + str(i) for i in range(num_clients)}
        self.clients = {
            'client_agent' + str(i): ClientAgent(agent_number=i,
                                                 train_datasets=client_to_datasets['client_agent' + str(i)],
                                                 evaluator=ModelEvaluator(X_test, y_test),
                                                 active_clients=active_clients) for i in
            range(num_clients)}  # initialize the agents

        self.server_agents = {'server_agent' + str(i): ServerAgent(agent_number=i) for i in
                              range(num_servers)}  # initialize servers

        # create directory with mappings from names to instances
        self.directory = Directory(clients=self.clients, server_agents=self.server_agents)

        for agent_name, agent in self.clients.items():
            agent.set_directory(self.directory)
            agent.initializations()
        for agent_name, agent in self.server_agents.items():
            agent.set_directory(self.directory)

        # OFFLINE diffie-helman key exchange
        # NOTE: this is sequential in implementation, but simulated as occuring parallel
        if config.USE_SECURITY:
            key_exchange_start = datetime.datetime.now()  # measuring how long the python script takes
            max_latencies = []
            for client_name, client in self.clients.items():
                # not including logic of sending/receiving public keys in latency computation since it is nearly zero
                client.send_pubkeys()
                max_latency = max(config.LATENCY_DICT[client_name].values())
                max_latencies.append(max_latency)
            simulated_time = max(max_latencies)

            key_exchange_end = datetime.datetime.now()  # measuring runtime
            key_exchange_duration = key_exchange_end - key_exchange_start
            simulated_time += key_exchange_duration
            if config.SIMULATE_LATENCIES:
                print(
                    'Diffie-helman key exchange simulated duration: {}\nDiffie-helman key exchange real run-time: {}\n'.format(
                        simulated_time, key_exchange_duration))

            for client_name, client in self.clients.items():
                client.initialize_common_keys()

    def run_simulation(self, num_iterations, server_agent_name='server_agent0'):
        """
        Online stage of simulation.
        :param num_iterations: number of iterations to run
        :param server_agent_name: which server to use. Defaults to first server.
        """
        # ONLINE
        server_agent = self.directory.server_agents[server_agent_name]
        server_agent.request_values(num_iterations=num_iterations)
        server_agent.final_statistics()
        for client_name, client in self.clients.items():
            print("Client :" + str(client.agent_number))
            print("Federated accuracy: " + str(client.federated_accuracy))
            print("Personal accuracy: " + str(client.personal_accuracy))

