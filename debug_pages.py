import os

print("Project root:", os.getcwd())

print("\nListing pages/ directory:")
if os.path.exists("pages"):
    for f in os.listdir("pages"):
        print(" -", f)
else:
    print("pages/ folder NOT FOUND")

print("\nChecking for razorpay_checkout.py:")
print("Exists:", os.path.exists("pages/razorpay_checkout.py"))
