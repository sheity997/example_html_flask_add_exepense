# Import libraries
from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route(("/"),methods = ['GET'])
def get_transactions():
    return render_template("transactions.html", transactions=transactions)


# Create operation
@app.route(("/add"),methods =['GET','POST'])
def add_transaction():
    if request.method == "GET":
        return render_template("form.html")
    if request.method == "POST":
        transaction = {
            'id': len(transactions)+1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))

# Update operation
@app.route(("/edit/<int:transaction_id>"),methods =['GET','POST'])
def edit_transaction(transaction_id):
    if request.method == "GET":
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                return render_template("edit.html", transaction=transaction)
    if request.method == "POST":
        date = request.form['date']           # Get the 'date' field value from the form
        amount = float(request.form['amount'])# Get the 'amount' field value from the form and convert it to a float
            # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date       # Update the 'date' field of the transaction
                transaction['amount'] = amount   # Update the 'amount' field of the transaction
                break                            # Exit the loop once the transaction is found and updated
        # Redirect to the transactions list page after updating the transaction
        return redirect(url_for("get_transactions"))


# Delete operation
# Delete operation: Delete a transaction
# Route to handle the deletion of an existing transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)  # Remove the transaction from the transactions list
            break  # Exit the loop once the transaction is found and removed

    # Redirect to the transactions list page after deleting the transaction
    return redirect(url_for("get_transactions"))

@app.route(("/search"),methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        min_value = float(request.form['min_amount'])
        max_value = float(request.form['max_amount'])
        filtered_transactions = []
        for transaction in transactions:
            if transaction['amount'] < max_value and transaction['amount'] > min_value:
                filtered_transactions.append(transaction)
        return render_template("transactions.html", transactions=filtered_transactions)

    if request.method == "GET":
        return render_template("search.html")




# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088, debug=True)
    