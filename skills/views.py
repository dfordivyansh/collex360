from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Roadmap, RoadmapItem, Profile
from .forms import RoadmapForm


# Utility: give XP
def award_points(user, points=10):
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.xp += points
    # Streak check
    if profile.last_active == now().date():
        profile.streak += 1
    else:
        profile.streak = 1
    profile.last_active = now().date()
    profile.save()


@login_required
def dashboard(request):
    roadmaps = Roadmap.objects.filter(user=request.user)
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, "skills/dashboard.html", {"roadmaps": roadmaps, "profile": profile})


@login_required
def generate_roadmap(request):
    if request.method == "POST":
        form = RoadmapForm(request.POST)
        if form.is_valid():
            roadmap = form.save(commit=False)
            roadmap.user = request.user
            roadmap.save()

            # Pre-fill items (example for demo)
            starter_items = {
                "MERN Stack": [
                    "HTML5 & Semantic Elements",
                    "CSS3 (Flexbox, Grid, Animations)",
                    "JavaScript (ES6+, Async, DOM)",
                    "Git & GitHub Basics",
                    "React Fundamentals",
                    "React Hooks (useState, useEffect, useContext)",
                    "React Router",
                    "State Management (Redux / Context API)",
                    "Component Patterns & Props Drilling",
                    "REST API Integration",
                    "Node.js Basics",
                    "Express.js Fundamentals",
                    "Authentication (JWT, OAuth2)",
                    "MongoDB CRUD",
                    "Mongoose & Data Modeling",
                    "Error Handling & Middleware",
                    "File Uploads",
                    "Security (Helmet, CORS, Rate Limiting)",
                    "Testing (Jest, Mocha, Chai)",
                    "Real-time Apps (Socket.io)",
                    "GraphQL Basics",
                    "Dockerizing MERN Apps",
                    "CI/CD with GitHub Actions",
                    "Deployment (Render, AWS, Vercel)",
                    "Scalability & Best Practices"
                ],
                "MEAN Stack": [
                    "HTML, CSS, JavaScript",
                    "Bootstrap / Tailwind",
                    "Angular Basics",
                    "Angular Components & Directives",
                    "Angular Routing",
                    "Reactive Forms",
                    "RxJS & Observables",
                    "Angular Services & DI",
                    "Authentication with JWT",
                    "State Management (NgRx)",
                    "Node.js Fundamentals",
                    "Express.js APIs",
                    "MongoDB Integration",
                    "File Uploads",
                    "Angular + REST API",
                    "Unit Testing (Karma/Jasmine)",
                    "E2E Testing (Protractor)",
                    "Angular Material",
                    "GraphQL with Angular",
                    "Docker with Angular+Node",
                    "Caching with Redis",
                    "Microservices Basics",
                    "Real-time Angular Apps",
                    "Cloud Deployment (AWS/GCP)",
                    "Performance Optimization"
                ],
                "AI & Machine Learning": [
                    "Python Programming",
                    "Maths (Linear Algebra, Calculus, Probability)",
                    "Data Wrangling (Pandas, NumPy)",
                    "Data Visualization (Matplotlib, Seaborn)",
                    "EDA (Exploratory Data Analysis)",
                    "Supervised Learning Algorithms",
                    "Unsupervised Learning Algorithms",
                    "Model Evaluation & Metrics",
                    "Feature Engineering",
                    "Overfitting & Regularization",
                    "Scikit-learn Toolkit",
                    "Neural Networks (ANN Basics)",
                    "Deep Learning (TensorFlow/Keras)",
                    "CNNs for Computer Vision",
                    "RNNs & LSTMs",
                    "Transformers & Attention",
                    "NLP (NLTK, SpaCy, HuggingFace)",
                    "Reinforcement Learning",
                    "MLOps Basics",
                    "Hyperparameter Tuning",
                    "Deployment with Flask/FastAPI",
                    "Model Monitoring",
                    "AutoML Tools",
                    "Edge AI",
                    "Ethics in AI"
                ],
                "Python Development": [
                    "Python Basics & Syntax",
                    "Data Structures & Algorithms",
                    "OOP Concepts",
                    "File Handling",
                    "Virtual Environments",
                    "Error & Exception Handling",
                    "Modules & Packages",
                    "Decorators & Generators",
                    "Web Scraping (Requests, BeautifulSoup)",
                    "Testing with PyTest",
                    "Django Basics",
                    "Django ORM",
                    "Django REST Framework",
                    "Authentication & Permissions",
                    "Database Integrations (Postgres/MySQL)",
                    "Flask Basics",
                    "FastAPI",
                    "Asynchronous Programming (AsyncIO)",
                    "Celery for Background Jobs",
                    "WebSockets",
                    "Docker with Python",
                    "CI/CD Integration",
                    "Cloud Deployment (AWS Lambda, Heroku)",
                    "API Security",
                    "Scaling Django Apps"
                ],
                "Data Analytics": [
                    "Excel & Google Sheets",
                    "SQL Queries",
                    "Advanced SQL (Joins, Window Functions)",
                    "Python for Data Analysis",
                    "NumPy & Pandas",
                    "Data Cleaning",
                    "EDA (Exploratory Data Analysis)",
                    "Visualization (Matplotlib, Seaborn, Plotly)",
                    "Tableau / Power BI Basics",
                    "Advanced Dashboards",
                    "Business Metrics & KPIs",
                    "Hypothesis Testing",
                    "Regression Models",
                    "Time Series Analysis",
                    "Clustering Analysis",
                    "Big Data (Hadoop, Spark)",
                    "Cloud Data Warehouses (Redshift, BigQuery)",
                    "ETL Concepts",
                    "Data Pipelines (Airflow, Luigi)",
                    "Data Quality Checks",
                    "A/B Testing",
                    "Data Governance",
                    "Data Security & Privacy",
                    "Storytelling with Data",
                    "Case Studies & Real Projects"
                ],
                "Cloud Computing": [
                    "Cloud Basics (IaaS, PaaS, SaaS)",
                    "Virtualization",
                    "Networking in Cloud",
                    "AWS Core Services (EC2, S3, IAM)",
                    "AWS RDS & DynamoDB",
                    "AWS Lambda",
                    "GCP Basics (Compute, Storage, BigQuery)",
                    "Azure Basics (VMs, Blob Storage, CosmosDB)",
                    "Containers (Docker)",
                    "Kubernetes Basics",
                    "CI/CD in Cloud",
                    "Infrastructure as Code (Terraform, CloudFormation)",
                    "Monitoring & Logging",
                    "Load Balancing & Auto-scaling",
                    "Cloud Security",
                    "Cloud Cost Optimization",
                    "Hybrid Cloud",
                    "Serverless Architectures",
                    "Edge Computing",
                    "Cloud AI Services",
                    "Data Lakes & Data Warehouses",
                    "API Gateways",
                    "DevOps in Cloud",
                    "Disaster Recovery",
                    "Compliance & Governance"
                ],
                "Cybersecurity": [
                    "Networking Fundamentals",
                    "Linux for Security",
                    "Firewalls & IDS/IPS",
                    "Cryptography",
                    "Hashing & Encryption",
                    "OWASP Top 10",
                    "SQL Injection",
                    "XSS & CSRF",
                    "Brute Force Attacks",
                    "Authentication Protocols",
                    "Penetration Testing",
                    "Bug Bounty Basics",
                    "Metasploit Framework",
                    "Wireshark for Traffic Analysis",
                    "Kali Linux Tools",
                    "Ethical Hacking",
                    "Malware Analysis",
                    "Digital Forensics",
                    "Cloud Security",
                    "Zero Trust Security",
                    "SIEM Tools",
                    "Phishing & Social Engineering",
                    "IoT Security",
                    "Incident Response",
                    "Cybersecurity Certifications"
                ],
                "DevOps": [
                    "Linux & Shell Scripting",
                    "Git & GitHub",
                    "CI/CD Concepts",
                    "Jenkins Pipelines",
                    "Containerization with Docker",
                    "Kubernetes Orchestration",
                    "Infrastructure as Code (Terraform, Ansible)",
                    "Monitoring (Prometheus, Grafana)",
                    "Log Management (ELK Stack)",
                    "Microservices Basics",
                    "Service Mesh (Istio)",
                    "Secrets Management (Vault)",
                    "Cloud DevOps (AWS/GCP/Azure)",
                    "Serverless CI/CD",
                    "Blue-Green Deployments",
                    "Canary Releases",
                    "Scaling & Load Balancing",
                    "Security in DevOps (DevSecOps)",
                    "GitOps (ArgoCD, Flux)",
                    "Automated Testing",
                    "Backup & Recovery",
                    "Observability",
                    "Chaos Engineering",
                    "Cost Optimization",
                    "Real-world Projects"
                ],
                "Blockchain": [
                    "Blockchain Fundamentals",
                    "Cryptography & Hash Functions",
                    "Bitcoin Concepts",
                    "Ethereum Basics",
                    "Ethereum Virtual Machine",
                    "Smart Contracts with Solidity",
                    "Gas & Transactions",
                    "Web3.js & Ethers.js",
                    "NFT Development",
                    "DeFi Protocols",
                    "Consensus Mechanisms",
                    "Proof of Work vs Proof of Stake",
                    "Polygon Layer-2",
                    "Solana Basics",
                    "Hyperledger Fabric",
                    "Smart Contract Security",
                    "DApp Development",
                    "Oracles",
                    "Cross-chain Bridges",
                    "Tokenomics",
                    "DAO Development",
                    "Stablecoins",
                    "Blockchain Scaling",
                    "Regulations & Compliance",
                    "Blockchain Real-world Projects"
                ],
                "Mobile App Development": [
                    "Java/Kotlin for Android",
                    "Swift/SwiftUI for iOS",
                    "Flutter Basics",
                    "React Native Basics",
                    "Dart Language",
                    "UI/UX Design for Mobile",
                    "APIs for Mobile Apps",
                    "Local Databases (SQLite, Room, CoreData)",
                    "Authentication & Firebase",
                    "Push Notifications",
                    "Camera & Sensors",
                    "Maps & Location",
                    "Offline-first Apps",
                    "Animations & Transitions",
                    "Testing Mobile Apps",
                    "App Store Deployment",
                    "Play Store Deployment",
                    "CI/CD for Mobile Apps",
                    "Mobile Security",
                    "AR/VR in Mobile",
                    "Cross-platform Challenges",
                    "Performance Optimization",
                    "Mobile Payments Integration",
                    "App Analytics",
                    "Real Projects"
                ],
                "UI/UX Design": [
                    "Design Principles",
                    "Color Theory",
                    "Typography",
                    "Grids & Layouts",
                    "Wireframing",
                    "Prototyping",
                    "Figma Basics",
                    "Adobe XD",
                    "User Personas",
                    "Design Systems",
                    "Material Design",
                    "Human-centered Design",
                    "Accessibility",
                    "Interaction Design",
                    "Usability Testing",
                    "Responsive Design",
                    "Mobile-first Design",
                    "Microinteractions",
                    "Gamification in UI",
                    "Dark Mode Design",
                    "Motion Design",
                    "AR/VR UX",
                    "Design Handoff",
                    "Portfolio Projects",
                    "Design Thinking Workshops"
                ],
                "AR/VR Development": [
                    "3D Modeling Basics",
                    "Unity Basics",
                    "Unreal Engine Basics",
                    "C# for Unity",
                    "Blueprints in Unreal",
                    "Physics Engines",
                    "VR Hardware Basics",
                    "ARKit & ARCore",
                    "OpenXR",
                    "WebXR APIs",
                    "360 Video Integration",
                    "3D Animation",
                    "Shaders & Materials",
                    "Spatial Audio",
                    "Interaction Design in VR",
                    "VR Optimizations",
                    "AR Navigation Apps",
                    "AR Filters & Lenses",
                    "Metaverse Basics",
                    "VR Multiplayer",
                    "AI in AR/VR",
                    "XR Cloud Services",
                    "VR Motion Sickness Handling",
                    "Publishing AR/VR Apps",
                    "Portfolio Projects"
                ],
                "Data Science": [
                    "Python for Data Science",
                    "Statistics & Probability",
                    "Linear Algebra for DS",
                    "Data Preprocessing",
                    "Feature Engineering",
                    "EDA Techniques",
                    "Visualization (Seaborn, Plotly)",
                    "SQL for Data Science",
                    "Machine Learning Basics",
                    "Supervised Learning",
                    "Unsupervised Learning",
                    "Deep Learning",
                    "NLP",
                    "Recommendation Systems",
                    "Big Data (Hadoop, Spark)",
                    "PySpark",
                    "Cloud Data Science",
                    "MLOps",
                    "Model Deployment",
                    "Experiment Tracking",
                    "AutoML",
                    "Edge AI",
                    "Ethical AI",
                    "Real DS Projects",
                    "Case Studies"
                ],
                "Game Development": [
                    "Game Engines Basics",
                    "Unity Basics",
                    "Unreal Engine",
                    "C# for Unity",
                    "C++ for Unreal",
                    "2D Game Development",
                    "3D Game Development",
                    "Physics in Games",
                    "Shaders & Materials",
                    "Animations in Games",
                    "Character Design",
                    "Level Design",
                    "Sound Design",
                    "Multiplayer Networking",
                    "Game AI",
                    "Mobile Game Dev",
                    "AR/VR in Games",
                    "Game Monetization",
                    "Optimization for Performance",
                    "Publishing Games",
                    "Steam/PlayStore Deployments",
                    "Game Analytics",
                    "Cloud Gaming",
                    "Metaverse Games",
                    "Portfolio Projects"
                ]
            }

            for item in starter_items.get(roadmap.tech_stack, []):
                RoadmapItem.objects.create(roadmap=roadmap, title=item)

            return redirect("skills:dashboard")
    else:
        form = RoadmapForm()
    return render(request, "skills/generate.html", {"form": form})


@login_required
def roadmap_detail(request, roadmap_id):
    roadmap = get_object_or_404(Roadmap, id=roadmap_id, user=request.user)
    if request.method == "POST":
        item_id = request.POST.get("item_id")
        item = get_object_or_404(RoadmapItem, id=item_id, roadmap=roadmap)
        item.completed = not item.completed
        item.save()
        award_points(request.user, 10)
        return redirect("skills:roadmap_detail", roadmap_id=roadmap.id)

    return render(request, "skills/roadmap.html", {"roadmap": roadmap})


@login_required
def leaderboard(request):
    profiles = Profile.objects.order_by("-xp")[:10]
    return render(request, "skills/leaderboard.html", {"profiles": profiles})
