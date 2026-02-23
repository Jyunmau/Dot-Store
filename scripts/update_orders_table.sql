-- 添加缺失的列
ALTER TABLE orders ADD COLUMN IF NOT EXISTS order_no VARCHAR(32);
ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_method VARCHAR(32);
ALTER TABLE orders ADD COLUMN IF NOT EXISTS customer_account_id INTEGER;
ALTER TABLE orders ADD COLUMN IF NOT EXISTS cash_transaction_id INTEGER;
ALTER TABLE orders ADD COLUMN IF NOT EXISTS note TEXT;
ALTER TABLE orders ADD COLUMN IF NOT EXISTS deleted_by INTEGER;

-- 为现有订单生成订单号
UPDATE orders SET order_no = 'ORD' || to_char(created_at, 'YYYYMMDD') || LPAD(id::text, 6, '0') WHERE order_no IS NULL;

-- 创建唯一索引
CREATE UNIQUE INDEX IF NOT EXISTS ix_orders_order_no ON orders(order_no);

-- 设置order_no为非空
ALTER TABLE orders ALTER COLUMN order_no SET NOT NULL;

SELECT 'Orders table updated' as result;
