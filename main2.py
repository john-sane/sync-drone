from detection.detection import Detection

if __name__ == "__main__":
    # define Detection object with src = dev/video0
    stream = Detection(0)
    # stream settings
    stream.setup()
    stream.streaming()
