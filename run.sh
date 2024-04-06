CUDA_VISIBLE_DEVICES=0 python mgca_detector.py --devices 1 --dataset rsna --data_pct 1 --learning_rate 5e-4



CUDA_VISIBLE_DEVICES=0 python -m debugpy --listen 0.0.0.0:8007 --wait-for-client mgca_detector.py --devices 1 --dataset object_cxr --data_pct 1 --learning_rate 5e-4

50207


