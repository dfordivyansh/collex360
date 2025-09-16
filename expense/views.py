import datetime
from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Expense, CATEGORY_CHOICES


@login_required(login_url="signup")
def dashboard(request):
    user = request.user
    expenses = Expense.objects.filter(user=user).order_by("-date")

    # -----------------------------
    # Handle Edit / Delete / Amount Update
    # -----------------------------
    if request.method == "POST":
        action = request.POST.get("action")
        expense_id = request.POST.get("expense_id")

        if expense_id:
            expense = get_object_or_404(Expense, id=expense_id, user=user)

            if action == "delete":
                expense.delete()

            elif action == "edit":
                expense.title = request.POST.get("title", expense.title)

                # Convert amount safely (typed value)
                try:
                    expense.amount = Decimal(request.POST.get("amount"))
                except (TypeError, ValueError, InvalidOperation):
                    pass  # keep old amount if invalid

                expense.category = request.POST.get("category", expense.category)
                expense.notes = request.POST.get("notes", expense.notes)
                expense.save()

            elif action == "add_amount":
                try:
                    add_value = Decimal(request.POST.get("amount"))
                    expense.amount += add_value
                    expense.save()
                except (TypeError, ValueError, InvalidOperation):
                    pass

            elif action == "remove_amount":
                try:
                    remove_value = Decimal(request.POST.get("amount"))
                    expense.amount = max(Decimal("0.00"), expense.amount - remove_value)
                    expense.save()
                except (TypeError, ValueError, InvalidOperation):
                    pass

        return redirect("expense_dashboard")

    # -----------------------------
    # Stats & Insights
    # -----------------------------
    today = datetime.date.today()

    total_expense = expenses.aggregate(total=Sum("amount"))["total"] or 0
    monthly_expense = expenses.filter(
        date__year=today.year, date__month=today.month
    ).aggregate(total=Sum("amount"))["total"] or 0

    # Category-wise totals (single query)
    category_data = {
        cat: expenses.filter(category=cat).aggregate(total=Sum("amount"))["total"] or 0
        for cat in expenses.values_list("category", flat=True).distinct()
    }

    top_category = max(category_data, key=category_data.get) if category_data else None
    forecast = round((monthly_expense / today.day) * 30, 2) if monthly_expense else 0

    # AI Insights
    ai_insights = []
    if monthly_expense > 10000:
        ai_insights.append("⚠️ You are overspending this month.")
    if category_data.get("Food", 0) > 3000:
        ai_insights.append("🍔 High food expenses! Try cooking at home.")
    if not ai_insights:
        ai_insights.append("✅ Balanced spending this month. Keep it up!")

    return render(request, "expense/dashboard.html", {
        "expenses": expenses,
        "total_expense": total_expense,
        "monthly_expense": monthly_expense,
        "category_data": category_data,
        "top_category": top_category,
        "forecast": forecast,
        "ai_insights": ai_insights,
        "CATEGORY_CHOICES": CATEGORY_CHOICES,  # 👈 pass choices to template
    })



@login_required(login_url="signup")
def add_expense(request):
    if request.method == "POST":
        title = request.POST.get("title")
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        notes = request.POST.get("notes")
        date = request.POST.get("date")

        # Convert and validate amount
        try:
            amount = Decimal(amount)
        except (TypeError, ValueError, InvalidOperation):
            amount = Decimal("0.00")

        if not title or not category:
            return render(request, "expense/add_expense.html", {
                "error": "Title and Category are required",
                "CATEGORY_CHOICES": CATEGORY_CHOICES,
            })

        Expense.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            category=category,
            notes=notes,
            date=date or datetime.date.today()
        )
        return redirect("expense_dashboard")

    return render(request, "expense/add_expense.html", {
        "CATEGORY_CHOICES": CATEGORY_CHOICES
    })


@login_required(login_url="signup")
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-date")
    total_spent = expenses.aggregate(total=Sum("amount"))["total"] or 0
    return render(request, "expense/expense_list.html", {
        "expenses": expenses,
        "total_spent": total_spent,
    })
