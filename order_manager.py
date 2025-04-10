import json

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"


def load_data(filename: str) -> list:
    """讀取 JSON 資料，若不存在回傳空清單"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_orders(filename: str, orders: list) -> None:
    """儲存訂單至 JSON 檔案"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)


def calculate_order_total(order: dict) -> int:
    """計算訂單總金額"""
    return sum(item["price"] * item["quantity"] for item in order["items"])


def print_order_report(data: list, title="訂單報表", single=False) -> None:
    """顯示訂單報表"""
    if single:
        print("\n==================== 出餐訂單 ====================")
    else:
        print("\n==================== 訂單報表 ====================")
    for idx, order in enumerate(data, 1):
        if not single:
            print(f"訂單 #{idx}")
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("--------------------------------------------------")
        print("商品名稱 單價\t數量\t小計")
        print("--------------------------------------------------")
        total = calculate_order_total(order)
        for item in order["items"]:
            subtotal = item["price"] * item["quantity"]  
            print(f"{item['name']}\t {item['price']}\t{item['quantity']}\t{subtotal}")
        print("--------------------------------------------------")
        print(f"訂單總額: {total:,}")
        print("==================================================\n")


def add_order(orders: list) -> str:
    """新增訂單，並檢查錯誤"""
    order_id = input("請輸入訂單編號：").strip().upper()
    if any(o["order_id"] == order_id for o in orders):
        return f"=> 錯誤：訂單編號 {order_id} 已存在！"

    customer = input("請輸入顧客姓名：").strip()
    items = []

    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：").strip()
        if name == "":
            break

        while True:
            try:
                price_input = input("請輸入價格：").strip()
                price = int(price_input)
                if price < 0:
                    print("=> 錯誤：價格不能為負數，請重新輸入")
                    continue
                quantity_input = input("請輸入數量：").strip()
                quantity = int(quantity_input)
                if quantity <= 0:
                    print("=> 錯誤：數量必須為正整數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")

        items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })

    if not items:
        return "=> 至少需要一個訂單項目"

    orders.append({
        "order_id": order_id,
        "customer": customer,
        "items": items
    })
    return f"=> 訂單 {order_id} 已新增！"


def process_order(orders: list) -> tuple:
    """處理出餐，返回訊息與該筆訂單"""
    if not orders:
        return "=> 沒有待處理的訂單", None

    print("\n======== 待處理訂單列表 ========")
    for idx, order in enumerate(orders, 1):
        print(f"{idx}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("================================")

    while True:
        choice = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ").strip()
        if choice == "":
            return "=> 出餐取消", None
        if not choice.isdigit() or not (1 <= int(choice) <= len(orders)):
            print("=> 錯誤：請輸入有效的數字")
        else:
            idx = int(choice) - 1
            order = orders.pop(idx)
            return f"=> 訂單 {order['order_id']} 已出餐完成", order


def main() -> None:
    """主程式"""
    while True:
        print("***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")
        choice = input("請選擇操作項目(Enter 離開)：").strip()

        if choice == "":
            break

        if choice == "1":
            orders = load_data(INPUT_FILE)
            msg = add_order(orders)
            print(msg)
            if "已新增" in msg:
                save_orders(INPUT_FILE, orders)

        elif choice == "2":
            orders = load_data(INPUT_FILE)
            if not orders:
                print("=> 尚無訂單")
            else:
                print_order_report(orders)

        elif choice == "3":
            orders = load_data(INPUT_FILE)
            msg, completed_order = process_order(orders)
            print(msg)
            if completed_order:
                completed_orders = load_data(OUTPUT_FILE)
                completed_orders.append(completed_order)
                save_orders(INPUT_FILE, orders)
                save_orders(OUTPUT_FILE, completed_orders)
                print("出餐訂單詳細資料：")
                print_order_report([completed_order], single=True)

        elif choice == "4":
            break
        else:
            print("=> 請輸入有效的選項（1-4）")


if __name__ == "__main__":
    main()

