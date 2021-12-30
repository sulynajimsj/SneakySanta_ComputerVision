import mediapipe as mp 
import cv2
import numpy as np
import time
from pygame import mixer

cap = cv2.VideoCapture(0)

# If we exceed this position we lose
threshold_position = 220

# Currennt position
currentPos = 0
theSum = 0
duration, notCaught = 0, 1


# Time initialization
beginTime, endTime = 0, 0
initilaize = False
currentStart, currentEnd = 0, 0


win = 0
iscurrent, tsum = False, 0

# checking frames
isframe, frame_check = 0, False
played = 0


#Load the audio
mixer.init()
mixer.music.load('song.wav')


# Here we calculate the sum of user current position. We do this by adding the sum of all landmarks
def findSum(landmarkList):
	
	total = 0
	for i in range(11, 33):
		# We only look at landmarks of body not face
		# Meaning user does not lose if face moves
		total += (landmarkList[i].x * 480)

	return total

# Here we find the distance between ankle and hip
def findDistance(landmarkList):
	return (landmarkList[28].y*640 - landmarkList[24].y*640)


# .visibilty is a property of landmark object that checks is it is in the frame
def visibileornot(landmarkList):
	if (landmarkList[28].visibility > 0.7) and (landmarkList[24].visibility > 0.7):
		return True
	return False

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
drawing = mp.solutions.drawing_utils

pic1 = cv2.imread('pic1.png')
pic2 = cv2.imread('pic2.png')

current_window = pic1


while True:

	_, frm = cap.read()
	rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
	res = pose.process(rgb)
	frm = cv2.blur(frm, (5,5))
	drawing.draw_landmarks(frm, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)

	if not(frame_check):
		try:
			if visibileornot(res.pose_landmarks.landmark):
				isframe = 1
				frame_check = True
			else:
				isframe = 0
		except:
			print("user is not visible")

	if isframe == 1:
		if currentPos >= 32:
			print("WON")
			win = 1
			break

		if not(initilaize):
			if played == 0:

				mixer.music.play()
				played = 1
			else:
				mixer.music.unpause()
			current_window = pic1
			beginTime = time.time()
			endTime = beginTime
			duration = np.random.randint(3, 6)
			initilaize = True

		if (endTime - beginTime) <= duration:
			try:
				m = findDistance(res.pose_landmarks.landmark)
				if m < threshold_position:
					currentPos += 1

				print("current progress is : ", currentPos)
			except:
				print("Not visible")

			endTime = time.time()

		else:
			if not(iscurrent):
				iscurrent = True
				currentStart = time.time()
				currentEnd = currentStart
				current_window = pic2

				mixer.music.pause()
				theSum = findSum(res.pose_landmarks.landmark)

			if (currentEnd - currentStart) <= 3:
				tsum = findSum(res.pose_landmarks.landmark)
				currentEnd = time.time()
				if abs(tsum - theSum) > 150:
					print("DEAD ", abs(tsum - theSum))
					notCaught = 0

			else:
				initilaize = False
				iscurrent = False


		cv2.circle(current_window, ((60 + 20 * currentPos), 280), 15, (255, 255, 255), -1)

		mainWin = np.concatenate((cv2.resize(frm, (800,400)), current_window), axis=0)
		cv2.imshow("Main Window", mainWin)
		#cv2.imshow("window", frm)
		#cv2.imshow("light", currWindow)

	else:
		cv2.putText(frm, "Please be in frame fully", (20,200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (10,255,10), 4)
		cv2.imshow("window", frm)


	if cv2.waitKey(1) == 27 or notCaught == 0 or win == 1:
		cv2.destroyAllWindows()
		cap.release()
		break


frm = cv2.imread("caught.png")
fr2 = cv2.imread("victory.png")

if notCaught == 0:
	cv2.imshow("Lost", frm)

if win == 1:
	cv2.imshow("Winner", fr2)

cv2.waitKey(0)