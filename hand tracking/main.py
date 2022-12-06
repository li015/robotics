import cv2
import time

video = "http://192.168.50.39:8080/video"
cap =cv2.VideoCapture(video)
# cap.set(3, 1280)
# cap.set(4, 720)

while True:
    ret, frame = cap.read()
    cv2.imshow("Capturing",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# if __name__ == '__main__':
#  cv2.namedWindow("camera", 1)#建立視窗
#  # 開啟ip攝像頭
#  video = "http://192.168.50.39:8080"#通過IP攝像頭獲得手機IP
#  cap = cv2.VideoCapture(video)  # 設定視訊捕獲
#  #建立VideoWriter類物件
#  fourcc = cv2.VideoWriter_fourcc(*'DIVX')#在windows下fourcc取值為DIVX
#  fps =cap.get(cv2.CAP_PROP_FPS)#獲取幀率
#  size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), 
#          int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))#獲取幀大小

# #  out = cv2.VideoWriter('F:\\camera.avi',fourcc, fps, size)#第一項是視訊儲存路徑
#  while(cap.isOpened()):#判斷相機是否開啟
#     ret, frame = cap.read()#變數ret判斷視訊幀是否成功讀入；變數frame表示讀取到陣列型別的每一幀,實質是圖片
#     if cv2.waitKey(1) & 0xFF == ord('q'):#按q鍵退出
#         break
#     if  ret == True:
#         # out.write(frame)#儲存幀
#         cv2.imshow('frame', frame)#顯示幀
#  cap.release()#關閉相機
# #  out.release()
#  cv2.destroyWindow("camera")#關閉視窗