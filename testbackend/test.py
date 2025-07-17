import asyncio
import websockets
import os
from model import du_doan_benh # ✅ Import hàm từ model.py

async def handle_client(websocket):
    try:
        async for message in websocket:
            print("Câu hỏi:", message, flush=True)

            # ✅ Dự đoán bệnh từ mô hình
            tra_loi = du_doan_benh(message)

            # ✅ Gửi kết quả về client
            await websocket.send(tra_loi)
            await websocket.send("[END]")

    except websockets.exceptions.ConnectionClosed:
        print("Client đã ngắt kết nối", flush=True)
    except Exception as e:
        print(f"Lỗi: {e}", flush=True)

async def main():
    print("Đang khởi động WebSocket server...", flush=True)
    async with websockets.serve(handle_client, "0.0.0.0", int(os.environ.get('PORT', 8091))):
        print("Đã chạy tại ws://localhost:8091", flush=True)
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
