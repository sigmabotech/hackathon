from chardet import detect
from ultralytics import YOLO


model = YOLO("bestmodel.onnx")
results = model("output.png")

for result in results :
  boxes = result.boxes
  probs=  result.probs
  result.show()

  result.save(filename="result.png")