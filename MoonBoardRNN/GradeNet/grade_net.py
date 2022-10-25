"""
Adapted from Evaluate_Generated_Output_v3.py
"""
import pathlib
from sys import setprofile
import numpy as np
import os
import tensorflow as tf
import keras.backend as K
from keras.layers.core import Dense
from keras.layers import Flatten, LSTM, Masking
from keras.models import Model
from keras.layers import Input
from MoonBoardRNN.BetaMove.BetaMove import classify_and_reorganize_data_ga, route_to_x_vectors, x_vectors_to_matrix
from MoonBoardRNN.GradeNet.model_helper import convert_num_to_V_grade

from share.moonboard_util import MoonBoardRoute

class GradeNet:
	def __init__(self):
		self.__model = GradeNet.create_model()
		dirname = pathlib.Path(__file__).parent
		filepath = os.path.join(dirname, 'GradeNet.h5')
		self.load_pretrained_weights(filepath)

	def create_model():
		np.random.seed(0)
		tf.random.set_seed(0)
		inputs = Input(shape=(12, 22))
		mask = Masking(mask_value=0.).compute_mask(inputs)
		lstm0 = LSTM(20, activation='tanh', input_shape=(12, 22), kernel_initializer='glorot_normal', return_sequences='True')(inputs, mask=mask)
		dense1 = Dense(100, activation='relu', kernel_initializer='glorot_normal')(lstm0)
		dense2 = Dense(80, activation='relu', kernel_initializer='glorot_normal')(dense1)
		dense3 = Dense(75, activation='relu', kernel_initializer='glorot_normal')(dense2)
		dense4 = Dense(50, activation='relu', kernel_initializer='glorot_normal')(dense3)
		dense5 = Dense(20, activation='relu', kernel_initializer='glorot_normal')(dense4)
		dense6 = Dense(10, activation='relu', kernel_initializer='glorot_normal')(dense5)
		flat = Flatten()(dense6)
		softmax2 = Dense(10, activation='softmax', name='softmax2')(flat)
		lstm1 = LSTM(20, activation='tanh', kernel_initializer='glorot_normal', return_sequences=True)(dense6)
		lstm2 = LSTM(20, activation='tanh', kernel_initializer='glorot_normal')(lstm1)
		dense7 = Dense(15, activation='relu', kernel_initializer='glorot_normal', name='dense7')(lstm2)
		dense8 = Dense(15, activation='relu', kernel_initializer='glorot_normal', name='dense8')(dense7)
		softmax3 = Dense(10, activation='softmax', name='softmax2')(dense8)

		def custom_loss(layer):
			def loss(y_true, y_pred):
				loss1 = K.sparse_categorical_crossentropy(y_true, y_pred)
				loss2 = K.sparse_categorical_crossentropy(y_true, layer)
				return K.mean(loss1 + loss2, axis=-1)
			return loss

		GradeNet = Model(inputs=[inputs], outputs=[softmax3])
		GradeNet.compile(optimizer='adam',
						loss=custom_loss(softmax2),
						metrics=['sparse_categorical_accuracy'])
		return GradeNet

	def load_pretrained_weights(self, weights_path):
		self.__model.load_weights(weights_path)

	def grade_route(self, route: MoonBoardRoute) -> str:
		x_vectors = route_to_x_vectors(route)
		matrix = x_vectors_to_matrix(x_vectors)
		# TODO: NORMALIZE THE MATRIX
		container = np.array([matrix])
		pred = self.__model.predict(container).argmax(axis = 1)
		return convert_num_to_V_grade(pred[0])
