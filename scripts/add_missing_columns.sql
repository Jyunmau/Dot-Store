-- 添加缺失的列
ALTER TABLE ingredients ADD COLUMN IF NOT EXISTS min_stock NUMERIC(10, 2) DEFAULT 0;
ALTER TABLE ingredients ADD COLUMN IF NOT EXISTS cost_per_unit NUMERIC(10, 2) DEFAULT 0;
ALTER TABLE ingredients ADD COLUMN IF NOT EXISTS category VARCHAR(64);
ALTER TABLE ingredients ADD COLUMN IF NOT EXISTS supplier VARCHAR(128);
ALTER TABLE ingredients ADD COLUMN IF NOT EXISTS expiry_date DATE;
ALTER TABLE ingredients ADD COLUMN IF NOT EXISTS status VARCHAR(32) DEFAULT 'active';

-- 添加user_id列到stock_records如果不存在
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'stock_records' AND column_name = 'user_id') THEN
        ALTER TABLE stock_records ADD COLUMN user_id INTEGER REFERENCES users(id);
    END IF;
END $$;

SELECT 'Columns added successfully' as result;
