
import cv2 
import os
import mediapipe as mp
import numpy as np
from sqlalchemy import false
import tensorflow as tf  
import time
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout



threshold = 0.8 #ilalagay sa settings
mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities
colors = [(245,117,16), (117,245,16), (16,117,245),(211,117,16), (123,245,16), (117,245,16)]
actions = np.array(['def','def','def','def','def']) 
predictions = []


models_list = { 'gabi':'@20f_TE.h5','kahapon':'@20f_TE.h5','magandang':'@20f_TE.h5','ngayon':'@20f_TE.h5','umaga':'@20f_TE.h5', 
            'bilog':'@20f_S.h5','bituin':'@20f_S.h5','parisukat':'@20f_S.h5','tatsulok':'@20f_S.h5',
            'sino':'@20f_Q.h5','ano':'@20f_Q.h5','kailan':'@20f_Q.h5','saan':'@20f_Q.h5',
            'maynila':'@20f_P.h5','mundo':'@20f_P.h5','Pilipinas':'@20f_P.h5',
            'babae':'@20f_F.h5','kamag-anak':'@20f_F.h5','lalake':'@20f_F.h5','matanda':'@20f_F.h5',
            'hi hello':'@20f_CP.h5','mahal kita':'@20f_CP.h5','salamat':'@20f_CP.h5','ulit':'@20f_CP.h5',
            'itim':'@20f_C.h5','kayumanggi':'@20f_C.h5','lila':'@20f_C.h5','puti':'@20f_C.h5',
            'basa':'@20f_AV.h5','gusto':'@20f_AV.h5','hintay':'@20f_AV.h5','tingnan':'@20f_AV.h5'
}

action_list = {'TE' : (['gabi','kahapon','magandang','ngayon','umaga','void_empty','no_sign']),
                'S' : (['bilog','bituin','parisukat','tatsulok','void_empty','no_sign']),
                'Q' : (['sino','ano','kailan','saan','void_empty','no_sign']),
                'P' : (['maynila','mundo','Pilipinas','void_empty','no_sign']),
                'F' : (['babae','kamag-anak','lalake','matanda','void_empty','no_sign']),
                'CP' : (['hi hello','mahal kita','salamat','ulit','void_empty','no_sign']),
                'C' : (['itim','kayumanggi','lila','puti','void_empty','no_sign']),
                'AV' : (['basa','gusto','hintay','tingnan','void_empty','no_sign'])
}

WG_key = { 'gabi':'TE','kahapon':'TE','TE':'TE','ngayon':'TE','umaga':'TE', 
            'bilog':'S','bituin':'S','parisukat':'S','tatsulok':'S',
            'sino':'Q','ano':'Q','kailan':'Q','saan':'Q',
            'maynila':'P','mundo':'P','Pilipinas':'P',
            'babae':'F','kamag-anak':'F','lalake':'F','matanda':'F',
            'hi hello':'CP','mahal kita':'CP','salamat':'CP','ulit':'CP',
            'itim':'C','kayumanggi':'C','lila':'C','puti':'C',
            'basa':'AV','gusto':'AV','hintay':'AV','tingnan':'AV'
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

def predict_sign(word, cap):
    print (word)
    load_actions(word)
    load_model(word)
    sequence = []  #need iclear?
    predicted = False
    a = True
    frame_num = 0
    start = time.time()
    print("Start Time")
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while a and frame_num <200: #Pwede adjust frame_num to achieve 15 sec na waiting
            frame_num += 1
            print (frame_num)
            # Read feed
            ret, frame = cap.read()
            # Make detections
            image, results = mediapipe_detection(frame, holistic)
            # Draw landmarks
            draw_styled_landmarks(image, results)
            # 2. Prediction logic
            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]
            
            if len(sequence) == 30:
                res = model.predict(np.expand_dims(sequence, axis=0))[0]
                # print(actions[np.argmax(res)])
                predictions.append(np.argmax(res))        
            #3. Viz logic
                if np.unique(predictions[-10:])[0]==np.argmax(res): 
                    if res[np.argmax(res)] > threshold: 
                        print(actions[np.argmax(res)])
                        if actions[np.argmax(res)] == word:
                            predicted = True
                            print(predicted)
                            break 
            cv2.imshow('OpenCV Feed', frame) #image > frame
            
            # Break gracefully
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        # cap.release()
        # cv2.destroyAllWindows()
    end = time.time()       
    print('time elapse: '+ str(end - start))
    return predicted