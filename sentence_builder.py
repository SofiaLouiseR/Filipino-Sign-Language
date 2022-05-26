# from cv2 import resize
# from sklearn.utils import resample
# import main123

# import time
# import cv2
# from main123 import mp
# from main123 import np
# from main123 import tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense
# threshold = 0.89 #ilalagay sa settings
# mp_holistic = mp.solutions.holistic # Holistic model
# mp_drawing = mp.solutions.drawing_utils # Drawing utilities
# predictions = []
# cap2 = cv2.VideoCapture(1)
# actions = np.array(['_confirm', '_wrong','void_empty','no_sign','ngayon','paalam','ulit'])
# hidden_words = np.array(['_confirm','void_empty','no_sign'])
# # delete? PassBy na lang? 
# # Get Item sa local

# def aa():
#     print('aa')
# def bb():
#     print('bb')

# model = Sequential()
# model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=( 30,1662)))
# model.add(LSTM(128, return_sequences=True, activation='relu'))
# model.add(LSTM(64, return_sequences=False, activation='relu'))
# model.add(Dense(64, activation='relu'))
# model.add(Dense(32, activation='relu'))
# model.add(Dense(actions.shape[0], activation='softmax'))
# model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# model.load_weights('FSL\Model\@Test_7 signs.h5')

# def mediapipe_detection(image, model):
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
#     image.flags.writeable = False                  # Image is no longer writeable
#     results = model.process(image)                 # Make prediction
#     image.flags.writeable = True                   # Image is now writeable 
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
#     return image, results

# def draw_styled_landmarks(image, results):
#     # Draw face connections
#     mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
#                              mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
#                              mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
#                              ) 
#     # Draw pose connections
#     mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
#                              mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=2), 
#                              mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=1)
#                              ) 
#     # Draw left hand connections
#     mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
#                              mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=2), 
#                              mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=1)
#                              ) 
#     # Draw right hand connections  
#     mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
#                              mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
#                              mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=1)
#                              )

                            

# def extract_keypoints(results):
#     pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
#     face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
#     lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
#     rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
#     return np.concatenate([pose, face, lh, rh])


# colors = [(245,117,16), (117,245,16), (16,117,245)]
# def prob_viz(res, actions, input_frame, colors):
#     output_frame = input_frame.copy()
#     for num, prob in enumerate(res):
#         cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
#         cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
#     return output_frame

# def open_camera(cap2):
    
#     # while True:  #Waiting sa input ng "START" 
#         ret,frame=cap2.read()
#         cv2.imshow('OpenCV Feed', frame)
#         k=cv2.waitKey(1)
#         # if k==ord('q'):
#         #     aa()
#         #     # cap2.release()
#         #     # cv2.destroyAllWindows()
            
#         #     break
        

# def sentence_builder(cap2):
#     sentence = []
#     blacklist = []
#     # res = any()

#     while True:
#         # out message
#         # open_camera(cap2)
        

#         word = predict_sign(cap2, sentence)
#         # sentence.append(predict_sign(cap2))
#         if word == '_wrong':
#             print ('wrong')
#             sentence = sentence[:-1]
            
#                 # print('empty sentence')
#         else:
#             if len(sentence) > 0:
#                 if word =='_wrong':
#                     print('wrong not append')

#                 if word != sentence[-1]:
#                     sentence.append(word)
#             else:
#                 sentence.append(word)
            
#             if len(sentence) > 5: 
#                     sentence = sentence[-5:]

#         print (sentence)

#     return



# def predict_sign(cap2,sentence):
    
#     sequence = []  #need iclear?
    
#     with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
#         while cap2.isOpened():
        
#             # Read feed
#             ret,frame = cap2.read()
            
#             # Make detections
#             image, results = mediapipe_detection(frame, holistic)

#             draw_styled_landmarks(image, results)
            
#             # 2. Prediction logic
#             keypoints = extract_keypoints(results)
#             sequence.append(keypoints)
#             sequence = sequence[-30:]
            
#             if len(sequence) == 30:
#                 res = model.predict(np.expand_dims(sequence, axis=0))[0]
                
#                 predictions.append(np.argmax(res))        
            
#                 if np.unique(predictions[-10:])[0]==np.argmax(res): 
#                     if res[np.argmax(res)] > threshold: 
#                         print('predicted: '+actions[np.argmax(res)])
#                         word = actions[np.argmax(res)]
#                         if word in hidden_words:
#                             print('hidden word')
#                         else:
#                             return word
                        
#             cv2.rectangle(frame, (0,0), (640, 40), (245, 117, 16), -1)
#             cv2.putText(frame, ' '.join(sentence), (3,30), 
#                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)    
#             cv2.imshow('OpenCV Feed', frame)
            
#             # Break gracefully
#             if cv2.waitKey(10) & 0xFF == ord('q'):
#                 break
#         cap2.release()
#         cv2.destroyAllWindows()


# # sentence_builder(cap2)