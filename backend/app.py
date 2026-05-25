from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

transactions = [
    {"id": 1, "type": "income", "category": "משכורת", "amount": 10000, "date": "2026-05-01"},
    {"id": 2, "type": "expense", "category": "שכר דירה", "amount": 4000, "date": "2026-05-02"},
    {"id": 3, "type": "expense", "category": "בילויים", "amount": 2500, "date": "2026-05-05"}
]

def generate_financial_advice(total_income, total_expense, entertainment_expense):
    balance = total_income - total_expense
    tips = []
    
    if balance < 0:
        tips.append("⚠️ אתה בגרעון החודש (מינוס)! מומלץ לעצור הוצאות לא חיוניות באופן מיידי.")
    elif balance > 0 and total_income > 0 and (balance / total_income) > 0.2:
        tips.append("🌟 כל הכבוד! אתה חוסך מעל 20% מההכנסה שלך. זה הזמן להשקיע את הכסף הפנוי.")
    else:
        tips.append("👍 המצב מאוזן, אך כדאי לנסות לצמצם הוצאות קטנות כדי להגדיל את החיסכון החודשי.")
        
    if total_income > 0:
        entertainment_percent = (entertainment_expense / total_income) * 100
        if entertainment_percent > 20:
            tips.append(f"💸 שים לב: הוצאות הבילויים שלך מהוות {entertainment_percent:.1f}% מההכנסה. מומלץ להציב גבול חודשי.")
            
    return tips

# התיקון כאן: השתמשתי ב-methods החוקי של פלאסק
@app.route('/api/finance', methods=['GET'])
def get_finance_data():
    total_income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    total_expense = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    entertainment_expense = sum(t['amount'] for t in transactions if t['category'] == 'בילויים')
    
    balance = total_income - total_expense
    advice = generate_financial_advice(total_income, total_expense, entertainment_expense)
    
    return jsonify({
        "transactions": transactions,
        "summary": {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        },
        "advice": advice
    })

@app.route('/api/finance', methods=['POST'])
def add_transaction():
    data = request.json
    if not data or 'type' not in data or 'category' not in data or 'amount' not in data:
        return jsonify({"error": "נתונים חסרים"}), 400
        
    new_transaction = {
        "id": len(transactions) + 1,
        "type": data['type'],
        "category": data['category'],
        "amount": float(data['amount']),
        "date": data.get('date', datetime.now().strftime("%Y-%m-%d"))
    }
    
    transactions.append(new_transaction)
    return jsonify(new_transaction), 201

@app.route('/api/finance/<int:tx_id>', methods=['DELETE'])
def delete_transaction(tx_id):
    global transactions
    transactions = [t for t in transactions if t['id'] != tx_id]
    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)