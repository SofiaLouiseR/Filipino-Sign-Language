
import cv2 
import os
import mediapipe as mp
import numpy as np
from sqlalchemy import false
import tensorflow as tf  
import time
from camera import cap
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout



threshold = 0.8 #ilalagay sa settings
mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities
colors = [(245,117,16), (117,245,16), (16,117,245),(211,117,16), (123,245,16), (117,245,16)]
actions = np.array(['def','def','def','def','def','def']) 
predictions = []


models_list = { 'gabi':'@20f_TE1.h5','kahapon':'@20f_TE1.h5','magandang':'@20f_TE2.h5','ngayon':'@20f_TE1.h5','umaga':'@20f_TE2.h5', 
            'bilog':'@20f_S1.h5','bituin':'@20f_S1.h5','parisukat':'@20f_S1.h5','tatsulok':'@20f_P.h5',
            'sino':'@20f_Q1.h5','ano':'@20f_Q2.h5','kailan':'@20f_Q1.h5','saan':'@20f_Q1.h5',
            'Maynila':'@20f_P.h5','mundo':'@20f_P.h5','Pilipinas':'@20f_P.h5',
            'babae':'@20f_F2.h5','kamag-anak':'@20f_F1.h5','lalake':'@20f_F1.h5','matanda':'@20f_F3.h5',
            'hi o hello':'@20f_F1.h5','mahal kita':'@20f_F2.h5','salamat':'@20f_CP1.h5','ulit':'@20f_CP2.h5',
            'itim':'@20f_Q2.h5','kayumanggi':'@20f_C.h5','lila':'@20f_C.h5','puti':'@20f_C.h5',
            'basa':'@20f_AV1.h5','gusto':'@20f_AV1.h5','hintay':'@20f_AV1.h5','tingnan':'@20f_AV2.h5'
}

action_list = {'TE1' : (['gabi','kahapon','magandang','ngayon','void_empty','no_sign']),
                'TE2' : (['kahapon','magandang','itim','umaga','void_empty','no_sign']),
                'S1' : (['bilog','bituin','parisukat','tatsulok','void_empty','no_sign']),
                'S2' : (['bilog','bituin','itim','tatsulok','void_empty','no_sign']),
                'Q1' : (['sino','ano','kailan','saan','void_empty','no_sign']),
                'Q2' : (['itim','ano','kailan','saan','void_empty','no_sign']),
                'P' : (['Maynila','mundo','Pilipinas','tatsulok','void_empty','no_sign']),
                'F1' : (['hi o hello','kamag-anak','lalake','matanda','void_empty','no_sign']),
                'F2' : (['babae','parisukat','mahal kita','bilog','void_empty','no_sign']),
                'F3' : (['matanda','parisukat','kamag-anak','saan','void_empty','no_sign']) ,
                'CP1' : (['hi o hello','mahal kita','salamat','ulit','void_empty','no_sign']),
                'CP2' : (['kayumanggi','puti','salamat','ulit','void_empty','no_sign']),
                'C1' : (['itim','kayumanggi','lila','puti','void_empty','no_sign']),
                'AV1' : (['basa','gusto','hintay','tingnan','void_empty','no_sign']),
                'AV2' : (['basa','gusto','mundo','tingnan','void_empty','no_sign'])
}

WG_key = { 'gabi':'TE1','kahapon':'TE1','magandang':'TE2','ngayon':'TE1','umaga':'TE2', 
            'bilog':'S1','bituin':'S1','parisukat':'S1','tatsulok':'P',
            'sino':'Q1','ano':'Q2','kailan':'Q1','saan':'Q1',
            'Maynila':'P','mundo':'P','Pilipinas':'P',
            'babae':'F2','kamag-anak':'F1','lalake':'F1','matanda':'F3',
            'hi o hello':'F1','mahal kita':'F2','salamat':'CP1','ulit':'CP2',
            'itim':'Q2','kayumanggi':'C1','lila':'C1','puti':'C1',
            'basa':'AV1','gusto':'AV1','hintay':'AV1','tingnan':'AV2'
}


model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=( 20,1662)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))
    
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

def load_actions(word):
    actions = np.array(action_list.get(WG_key.get(word))) 

def load_model(word):
    # print('model ay: ' + models_list.get(word))
    model.load_weights(os.path.join (r'models',models_list.get(word)))



def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

def draw_styled_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                             ) 
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=2), 
                             mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=1)
                             ) 
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=2), 
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=1)
                             ) 
    # Draw right hand connections  
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=1)
                             )

                        
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])



def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()
    for num, prob in enumerate(res):
        cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)    
    return output_frame

def open_camera(cap):
    
    while True:  #Waiting sa input ng "START" 
        ret,frame=cap.read()
        cv2.imshow("Frame", frame)
        k=cv2.waitKey(1)
        if k==ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

def predict_sign(word):
    # load_actions(word)
    actions = np.array(action_list.get(WG_key.get(word))) 
    print(actions)

    load_model(word)
    
    sequence = []
    sentence = []
    predictions = []

    predicted = False
    frame_num = 0
    
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True and frame_num <100: #Pwede adjust frame_num to achieve 15 sec na waiting
            frame_num += 1
            # print (frame_num)
            # Read feed
            ret, frame = cap.read()
            # Make detections
            image, results = mediapipe_detection(frame, holistic)
            # Draw landmarks
            draw_styled_landmarks(image, results)
            # 2. Prediction logic
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-20:]
            
            # if len(sequence) == 20:
            #     res = model.predict(np.expand_dims(sequence, axis=0))[0]
            #     # print(actions[np.argmax(res)])
            #     predictions.append(np.argmax(res))        
            # #3. Viz logic
            #     if np.unique(predictions[-10:])[0]==np.argmax(res): 
            #         if res[np.argmax(res)] > threshold: 
            #             print(actions[np.argmax(res)])
            #             if actions[np.argmax(res)] == word:
            #                 predicted = True
            #                 print(predicted)
            #                 break 

            if len(sequence) == 20:
                
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                print(actions[np.argmax(res)])
                predictions.append(np.argmax(res))
            #3. Viz logic
                if np.unique(predictions[-10:])[0]==np.argmax(res): 
                    if res[np.argmax(res)] > threshold: 
                        
                        if len(sentence) > 0: 
                            if actions[np.argmax(res)] != sentence[-1]:
                                sentence.append(actions[np.argmax(res)])
                        else:
                            sentence.append(actions[np.argmax(res)])

                if len(sentence) > 5: 
                    sentence = sentence[-5:]
                print(sentence)
                
                try:
                    print(sentence[-1])
                    print(word)
                    if sentence[-1] == word:
                        predicted = True
                        print(predicted)
                        break 
                except:
                    print('sentence is')





            # cv2.imshow('OpenCV Feed', frame) #image > frame
            
            # Break gracefully
            # if cv2.waitKey(10) & 0xFF == ord('q'):
            #     break
        # cap.release()
        # cv2.destroyAllWindows()
    
    return predicted