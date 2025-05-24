
import queue
import threading
import time
import uuid

# Simulated SQS Queue
class SimpleQueueService:
    def __init__(self):
        self.queue = queue.Queue()

    def send_message(self, message_body):
        message_id = str(uuid.uuid4())
        self.queue.put({"MessageId": message_id, "Body": message_body})
        print(f"📤 Sent: {message_body}")
        return message_id

    def receive_message(self, wait_time=2):
        try:
            msg = self.queue.get(timeout=wait_time)
            print(f"📥 Received: {msg['Body']}")
            return msg
        except queue.Empty:
            print("⌛ No messages in queue.")
            return None

# ------------------------
# 🔁 Producer + Consumer
# ------------------------
def producer(sqs):
    for i in range(3):
        sqs.send_message(f"Message #{i+1}")
        time.sleep(1)

def consumer(sqs):
    for _ in range(5):
        sqs.receive_message()
        time.sleep(2)

# Run simulation
if __name__ == "__main__":
    sqs = SimpleQueueService()
    t1 = threading.Thread(target=producer, args=(sqs,))
    t2 = threading.Thread(target=consumer, args=(sqs,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()
