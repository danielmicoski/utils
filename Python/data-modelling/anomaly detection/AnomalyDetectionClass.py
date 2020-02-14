from abc import ABC, abstractmethod 
import time
import matplotlib.pyplot as plt
import numpy
from sklearn import svm
from sklearn.datasets import make_moons, make_blobs
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

class AnomalyDetectionPipeline():
    def __init__(self, data, **kwargs):
        self.model_names = [key for key, value in kwargs.items()]
        self.model_values = [value for key, value in kwargs.items()]
        self.data = data

    def run(self, multiple_plots=False):
        plot_num = 1
        plt.figure(figsize=(len(self.model_names) * 2 + 3, 12.5))
        plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.2, hspace=.01)
        plt.yticks(())
        for model in range(0,len(self.model_names)):
            print('Running '+self.model_names[model])
            model_run = self.model_values[model]
            model_run.fit()
            y_pred = model_run.predict()
            if multiple_plots == True:
                plt.subplot(1, len(self.model_names), plot_num)
                colors = numpy.array(['#377eb8', '#ff7f00'])
                plt.scatter(self.data[:, 0], self.data[:, 1], s=10, color=colors[(y_pred + 1) // 2])
                plt.xlim(-7, 7)
                plt.ylim(-7, 7)
                plt.title(self.model_names[model])
                plt.text(.99, .01, str(round(model_run.getIntervalTime(),2))+'s',
                        transform=plt.gca().transAxes, size=12,
                        horizontalalignment='right')
                plot_num += 1
            else:
                print(model_run.plot(show=True, savefig=True))
        plt.show()

class AnomalyDetectionAlgorithm(ABC):
    '''
    DocString
    '''
    def fit(self, model,values):
        return model.fit(values)

    @abstractmethod
    def predict(self):
        pass
    
    def plot(self, name, show, savefig):
        colors = numpy.array(['#377eb8', '#ff7f00'])
        fig = plt.figure()
        plot_name = name
        plt.title(plot_name)
        plot = plt.scatter(self.values[:, 0], self.values[:, 1], s=10, color=colors[(self.predict() + 1) // 2])
        if savefig != None:
            try:   
                fig.savefig(plot_name+'.png')
            except:
                print('Erro')
        if show==False:
            return plot
        return plt.show()

    def getTime(self):
        return time.time()

    def getIntervalTime(self,interval):
        return interval

    def getModel(self, model):
        return model


class EllipticEnvelopeAlgo(AnomalyDetectionAlgorithm):
    '''
    DocString
    '''

    def __init__(self,values,outliers_fraction):
        self.values = values
        self.outliers_fraction = outliers_fraction
        self.model = EllipticEnvelope(contamination=outliers_fraction)
        self.time = 0
        
    def fit(self):
        t0 = super().getTime()
        super().fit(self.model, self.values)
        t1 = super().getTime()
        self.time = t1-t0
        return None
    
    def predict(self):
        return self.model.fit(self.values).predict(self.values)

    def plot(self, show=False, savefig=True):
        super().plot('EllipticEnvelope', show, savefig)

    def getModel(self):
        return super().getModel(self.model)

    def getIntervalTime(self):
        return super().getIntervalTime(self.time)


class OneClassSVMAlgo(AnomalyDetectionAlgorithm):
    '''
    DocString
    '''
    model = None
    time = 0

    def __init__(self,values,outliers_fraction,kernel="rbf",gamma=0.1):
        self.values = values
        self.outliers_fraction = outliers_fraction
        self.model = svm.OneClassSVM(nu=outliers_fraction, kernel=kernel,gamma=gamma)
    
    def fit(self):
        t0 = super().getTime()
        super().fit(self.model, self.values)
        t1 = super().getTime()
        self.time = t1-t0
        return None
    
    def predict(self):
        return self.model.fit(self.values).predict(self.values)

    def plot(self, show=False, savefig=True):
        super().plot('OneClassSVM', show, savefig)

    def getModel(self):
        return super().getModel(self.model)

    def getIntervalTime(self):
        return super().getIntervalTime(self.time)
        

class IsolationForestAlgo(AnomalyDetectionAlgorithm):
    '''
    DocString
    '''
    model = None
    time = 0

    def __init__(self,values,outliers_fraction, random_state=42):
        self.values = values
        self.outliers_fraction = outliers_fraction
        self.model = IsolationForest(contamination=outliers_fraction, random_state=random_state)
    
    def fit(self):
        t0 = super().getTime()
        super().fit(self.model, self.values)
        t1 = super().getTime()
        self.time = t1-t0
        return None
    
    def predict(self):
        return self.model.fit(self.values).predict(self.values)

    def plot(self, show=False, savefig=True):
        super().plot('IsolationForest', show, savefig)

    def getModel(self):
        return super().getModel(self.model)

    def getIntervalTime(self):
        return super().getIntervalTime(self.time)

class LocalOutlierFactorAlgo(AnomalyDetectionAlgorithm):
    '''
    DocString
    '''
    model = None
    time = 0

    def __init__(self,values,outliers_fraction,n_neighbors=35):
        self.values = values
        self.outliers_fraction = outliers_fraction
        self.model = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=outliers_fraction)
    
    def fit(self):
        t0 = super().getTime()
        super().fit(self.model, self.values)
        t1 = super().getTime()
        self.time = t1-t0
        return None
    
    def predict(self):
        return self.model.fit_predict(self.values)

    def plot(self, show=False, savefig=None):
        super().plot('LocalOutlierFactor', show, savefig)

    def getModel(self):
        return super().getModel(self.model)

    def getIntervalTime(self):
        return super().getIntervalTime(self.time)
