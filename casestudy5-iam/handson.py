
import fnmatch

class Policy:
    def __init__(self, statements):
        self.statements = statements

    def allows(self, action, resource):
        for stmt in self.statements:
            if (fnmatch.fnmatch(action, stmt["Action"]) and 
                fnmatch.fnmatch(resource, stmt["Resource"])):
                return stmt["Effect"] == "Allow"
        return False

class Role:
    def __init__(self, name, policy):
        self.name = name
        self.policy = policy

class User:
    def __init__(self, name):
        self.name = name
        self.roles = []

    def attach_role(self, role):
        self.roles.append(role)

    def is_allowed(self, action, resource):
        for role in self.roles:
            if role.policy.allows(action, resource):
                print(f"✅ Allowed by role: {role.name}")
                return True
        print(f"⛔ Denied for: {self.name}")
        return False

# -----------------------------
# 🧪 Example: Setup IAM Graph
# -----------------------------
read_only_policy = Policy([
    {"Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::my-bucket/*"}
])

admin_policy = Policy([
    {"Effect": "Allow", "Action": "*", "Resource": "*"}
])

# Create roles
reader_role = Role("S3ReadOnly", read_only_policy)
admin_role = Role("Admin", admin_policy)

# Create users
alice = User("Alice")
bob = User("Bob")

alice.attach_role(reader_role)
bob.attach_role(admin_role)

# -----------------------------
# 🔍 Test Permissions
# -----------------------------
alice.is_allowed("s3:GetObject", "arn:aws:s3:::my-bucket/file1.txt")   # ✅
alice.is_allowed("s3:PutObject", "arn:aws:s3:::my-bucket/file2.txt")   # ⛔
bob.is_allowed("s3:PutObject", "arn:aws:s3:::my-bucket/file2.txt")     # ✅
