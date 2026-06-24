from faker import Faker
import pandas as pd
import random

fake = Faker('en_IN')

vendor_categories = [
    "Tower Maintenance","Fiber Operations","Network Equipment",
    "Managed Services","Cloud Services","Data Center Services",
    "Power Infrastructure","Field Operations","IT Support",
    "Cyber Security Services","NOC Operations","RF Optimization"
]
circles = [
    "Delhi","Noida","Gurugram","Chandigarh","Mohali","Odisha",
    "Punjab","Haryana","Rajasthan","Mumbai","Maharashtra",
    "Karnataka","Tamil Nadu","Kerala","Andhra Pradesh","Telangana",
    "West Bengal","Assam","Bihar","UP East","UP West",
    "Madhya Pradesh","Gujarat"
]
criticality     = ["Critical","High","Medium","Low"]
regions         = ["North","South","East","West"]
data_access     = ["Public","Internal","Confidential","Sensitive"]
assessment_freq = ["Monthly","Quarterly","Half-Yearly","Annually"]
review_status   = ["Open","Under Review","Mitigation In Progress","Closed"]


def generate_vendor_fields(profile: str) -> dict:
    if profile == "critical":
        return dict(
            Critical_Findings       = random.choices(range(6,11),  weights=[10,20,30,25,15])[0],
            High_Findings           = random.choices(range(8,21),  weights=[15,15,14,12,10,9,8,6,4,3,2,1,1])[0],
            Open_Risks              = random.choices(range(6,21),  weights=[15,14,13,12,11,10,8,6,4,3,2,1,1,0,0])[0],
            Compliance_Score        = random.choices([40,45,50,55,60,65], weights=[10,15,20,25,20,10])[0],
            VAPT_Findings           = random.choices(range(5,11),  weights=[20,20,18,16,14,12])[0],
            Patch_Compliance        = random.randint(40, 65),
            MFA_Enabled             = random.choices(["Yes","No"], weights=[20,80])[0],
            DLP_Violations          = random.choices([3,4,5,6,7],  weights=[25,25,20,15,15])[0],
            Security_Incidents      = random.choices([3,4,5],      weights=[50,30,20])[0],
            SLA_Breaches            = random.choices([3,4,5],      weights=[50,30,20])[0],
            Mitigation_Overdue_Days = random.choices([60,90,120,150,180], weights=[20,25,25,20,10])[0],
        )
    elif profile == "high":
        return dict(
            Critical_Findings       = random.choices(range(3,7),   weights=[30,30,25,15])[0],
            High_Findings           = random.choices(range(5,15),  weights=[15,15,14,13,12,10,8,6,4,3])[0],
            Open_Risks              = random.choices(range(4,12),  weights=[20,18,16,14,12,10,6,4])[0],
            Compliance_Score        = random.choices([60,65,70,75,80], weights=[15,20,30,25,10])[0],
            VAPT_Findings           = random.choices(range(3,8),   weights=[25,25,20,18,12])[0],
            Patch_Compliance        = random.randint(60, 78),
            MFA_Enabled             = random.choices(["Yes","No"], weights=[50,50])[0],
            DLP_Violations          = random.choices([1,2,3,4],    weights=[30,35,25,10])[0],
            Security_Incidents      = random.choices([1,2,3],      weights=[45,35,20])[0],
            SLA_Breaches            = random.choices([1,2,3],      weights=[45,35,20])[0],
            Mitigation_Overdue_Days = random.choices([30,45,60,90], weights=[30,30,25,15])[0],
        )
    elif profile == "medium":
        return dict(
            Critical_Findings       = random.choices(range(0,4),   weights=[35,35,20,10])[0],
            High_Findings           = random.choices(range(2,10),  weights=[20,20,18,15,12,8,4,3])[0],
            Open_Risks              = random.choices(range(2,9),   weights=[20,20,18,16,13,8,5])[0],
            Compliance_Score        = random.choices([70,75,80,85,90], weights=[15,20,30,25,10])[0],
            VAPT_Findings           = random.choices(range(1,6),   weights=[30,28,22,13,7])[0],
            Patch_Compliance        = random.randint(72, 88),
            MFA_Enabled             = random.choices(["Yes","No"], weights=[70,30])[0],
            DLP_Violations          = random.choices([0,1,2],      weights=[45,35,20])[0],
            Security_Incidents      = random.choices([0,1,2],      weights=[55,30,15])[0],
            SLA_Breaches            = random.choices([0,1,2],      weights=[55,30,15])[0],
            Mitigation_Overdue_Days = random.choices([0,15,30,45], weights=[35,30,25,10])[0],
        )
    else:  
        return dict(
            Critical_Findings       = random.choices([0,1],        weights=[80,20])[0],
            High_Findings           = random.choices(range(0,6),   weights=[40,28,17,9,4,2])[0],
            Open_Risks              = random.choices(range(0,6),   weights=[35,28,18,11,5,3])[0],
            Compliance_Score        = random.choices([80,85,90,95,100], weights=[10,20,30,25,15])[0],
            VAPT_Findings           = random.choices(range(0,4),   weights=[50,28,14,8])[0],
            Patch_Compliance        = random.randint(85, 100),
            MFA_Enabled             = random.choices(["Yes","No"], weights=[90,10])[0],
            DLP_Violations          = random.choices([0,1],        weights=[80,20])[0],
            Security_Incidents      = random.choices([0,1],        weights=[85,15])[0],
            SLA_Breaches            = random.choices([0,1],        weights=[85,15])[0],
            Mitigation_Overdue_Days = random.choices([0,15],       weights=[75,25])[0],
        )


PROFILE_DIST = [
    ("low",      350),
    ("medium",   350),
    ("high",     200),
    ("critical", 100),
]

profiles = []
for profile, count in PROFILE_DIST:
    profiles.extend([profile] * count)
random.shuffle(profiles)

vendors = []
for i, profile in enumerate(profiles):
    f = generate_vendor_fields(profile)

    vendors.append({
        "Vendor_ID":               f"V{i+1:04}",
        "Vendor_Name":             fake.company(),
        "Vendor_Category":         random.choice(vendor_categories),
        "Vendor_Circle":           random.choice(circles),
        "Service_Criticality":     random.choice(criticality),
        "Region":                  random.choice(regions),
        "Critical_Findings":       f["Critical_Findings"],
        "High_Findings":           f["High_Findings"],
        "Open_Risks":              f["Open_Risks"],
        "Compliance_Score":        f["Compliance_Score"],
        "VAPT_Findings":           f["VAPT_Findings"],
        "Patch_Compliance":        f["Patch_Compliance"],
        "MFA_Enabled":             f["MFA_Enabled"],
        "Data_Access_Level":       random.choice(data_access),
        "DLP_Violations":          f["DLP_Violations"],
        "Security_Incidents":      f["Security_Incidents"],
        "SLA_Breaches":            f["SLA_Breaches"],
        "Mitigation_Overdue_Days": f["Mitigation_Overdue_Days"],
        "Last_Assessment_Date":    fake.date_between(start_date='-365d', end_date='today'),
        "Assessment_Frequency":    random.choice(assessment_freq),
        "Risk_Review_Status":      random.choice(review_status),
        # No score, no tier — that's risk_engine.py's job
    })

df = pd.DataFrame(vendors)
df.to_csv("../data/vendors.csv", index=False)

print(f"Generated {len(df)} vendors")
print(df.head())