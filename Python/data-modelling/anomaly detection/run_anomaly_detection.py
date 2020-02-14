from AnomalyDetectionClass import EllipticEnvelopeAlgo,OneClassSVMAlgo,IsolationForestAlgo,LocalOutlierFactorAlgo,AnomalyDetectionPipeline
outliers_fraction = 0.1

 

pipe = AnomalyDetectionPipeline(
    data = A,
    elliptic_model = EllipticEnvelopeAlgo(A, outliers_fraction),
    svm_model = OneClassSVMAlgo(A, outliers_fraction),
    isolation_model = IsolationForestAlgo(A, outliers_fraction),
    lof_model = LocalOutlierFactorAlgo(A, outliers_fraction))

 

pipe.run(multiple_plots=True)