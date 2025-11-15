from django.contrib import admin
from .models import Draw, Ticket
from .services import quick_pick, score

@admin.action(description="선택 회차 추첨(DONE으로 전환)")
def admin_draw_action(modeladmin, request, queryset):
    for draw in queryset:
        if draw.winning_numbers:
            continue
        draw.winning_numbers = quick_pick()
        draw.status = "DONE"
        draw.save(update_fields=["winning_numbers", "status"])

@admin.action(description="선택 회차 정산(등수/일치수 저장)")
def admin_settle_action(modeladmin, request, queryset):
    for draw in queryset:
        if not draw.winning_numbers:
            continue
        tickets = Ticket.objects.filter(draw=draw)
        for t in tickets:
            r = score(t.picks, draw.winning_numbers)
            t.match_count, t.rank = r["match_count"], r["rank"]
            t.save(update_fields=["match_count", "rank"])

@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = ("number", "draw_date", "status", "winning_numbers")
    list_filter = ("status",)
    search_fields = ("number",)
    actions = [admin_draw_action, admin_settle_action]  # ← 액션 연결

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("user", "draw", "is_auto", "picks", "match_count", "rank", "purchased_at")
    list_filter = ("draw", "is_auto", "rank")
    search_fields = ("user__username",)