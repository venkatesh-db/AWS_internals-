
import threading
import time
from collections import defaultdict

# Simulated In-Memory DynamoDB Table

class DynamoDBSim:
    def __init__(self, replica_count=3):
        self.lock = threading.Lock()
        #[defualt dict 3 ]
        self.replicas = [defaultdict(dict) for _ in range(replica_count)]
        self.replica_count = replica_count

    def _replicate_write(self, partition_key, sort_key, value):
        for replica in self.replicas:
            with self.lock:
                replica[partition_key][sort_key] = value

    def put_item(self, partition_key, sort_key, value):
        
        print(f"📝 Writing ({partition_key}, {sort_key}) = {value} to {self.replica_count} replicas")
        
        thread = threading.Thread(target=self._replicate_write, args=(partition_key, sort_key, value))
        thread.start()
        thread.join()
        
        print("✅ Write replicated to all nodes (quorum)")

    def get_item(self, partition_key, sort_key):
        results = []
        for replica in self.replicas:
            with self.lock:
                item = replica.get(partition_key, {}).get(sort_key)
                if item:
                    results.append(item)
        if results:
            # Majority read consistency
            majority_item = max(set(results), key=results.count)
            print(f"📦 Read quorum result: {majority_item}")
            return majority_item
        else:
            print("❌ Item not found")
            return None

# -------------------------
# 🔁 Usage Example
# -------------------------
if __name__ == "__main__":
    
    db = DynamoDBSim(replica_count=3)

    # Write data
    db.put_item("user#101", "email", "venkatesh@example.com")

    time.sleep(1)

    # Read data
    db.get_item("user#101", "email")
