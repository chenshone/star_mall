-- Category Data
INSERT INTO category (name, parent_category_id, level, is_tab, add_time, is_deleted, update_time) VALUES
('家用电器', NULL, 1, TRUE, NOW(), FALSE, NOW()),
('厨房电器', 1, 2, FALSE, NOW(), FALSE, NOW()),
('电饭煲', 2, 3, FALSE, NOW(), FALSE, NOW()),
('个护健康', NULL, 1, FALSE, NOW(), FALSE, NOW()),
('按摩器械', 4, 2, FALSE, NOW(), FALSE, NOW()),
('电动按摩椅', 5, 3, FALSE, NOW(), FALSE, NOW());

Brands Data
INSERT INTO brands (name, logo, add_time, is_deleted, update_time) VALUES
('苹果', 'apple_logo.png', NOW(), FALSE, NOW()),
('华为', 'huawei_logo.png', NOW(), FALSE, NOW()),
('小米', 'xiaomi_logo.png', NOW(), FALSE, NOW()),
('索尼', 'sony_logo.png', NOW(), FALSE, NOW());

-- Goods Data with more entries
INSERT INTO goods (category_id, brand_id, on_sale, goods_sn, name, click_num, sold_num, fav_num, market_price, shop_price, goods_brief, ship_free, images, desc_images, goods_front_image, is_new, is_hot, add_time, is_deleted, update_time) VALUES
(3, 1, TRUE, 'SN10002', '小米电饭煲', 150, 110, 45, 500.00, 399.99, '智能电饭煲，容量大', TRUE, '["img3.png", "img4.png"]', '["dimg3.png", "dimg4.png"]', 'front_img2.png', TRUE, FALSE, NOW(), FALSE, NOW()),
(3, 2, TRUE, 'SN10003', '苹果电饭煲', 200, 155, 80, 800.00, 699.99, '多功能电饭煲，操作简便', TRUE, '["img5.png", "img6.png"]', '["dimg5.png", "dimg6.png"]', 'front_img3.png', FALSE, TRUE, NOW(), FALSE, NOW()),
(6, 3, TRUE, 'SN10004', '索尼按摩椅', 100, 40, 20, 3000.00, 2799.99, '高级豪华按摩椅', FALSE, '["img7.png", "img8.png"]', '["dimg7.png", "dimg8.png"]', 'front_img4.png', FALSE, TRUE, NOW(), FALSE, NOW());

-- GoodsCategoryBrand Data with more entries
INSERT INTO goodscategorybrand (category_id, brand_id, add_time, is_deleted, update_time) VALUES
(2, 1, NOW(), FALSE, NOW()),
(5, 2, NOW(), FALSE, NOW()),
(5, 3, NOW(), FALSE, NOW());

-- Banner Data
-- Banner Data with BaseModel fields
INSERT INTO banner (image, url, `index`, add_time, is_deleted, update_time) VALUES
('banner1.png', 'http://example.com/banner1', 1, NOW(), FALSE, NOW()),
('banner2.png', 'http://example.com/banner2', 2, NOW(), FALSE, NOW()),
('banner3.png', 'http://example.com/banner3', 3, NOW(), FALSE, NOW()),
('banner4.png', 'http://example.com/banner4', 4, NOW(), FALSE, NOW());
