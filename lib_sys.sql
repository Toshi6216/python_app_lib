DROP DATABASE IF EXISTS lib_sys; 
CREATE DATABASE IF Not EXISTS lib_sys;

USE lib_sys;

DROP TABLE IF EXISTS staff;

CREATE TABLE staff (
  id int not null, 
  staff_id VARCHAR(255) NOT NULL,
  s_pass VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
  user_id VARCHAR(255) NOT NULL,
  user_name VARCHAR(255) NOT NULL,
  count_books int not null,
  PRIMARY KEY (user_id)
);

DROP TABLE IF EXISTS books; 

CREATE TABLE books (
  book_id VARCHAR(255) NOT NULL,
  book_title VARCHAR(40) NOT NULL,
  is_borrowed BOOLEAN NOT NULL,
  borrowed_date DATE,
  return_date DATE,
  user_id VARCHAR(255),
  PRIMARY KEY (book_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id) 
  ON DELETE SET NULL ON UPDATE CASCADE
);

-- usersテーブルにダミーデータを挿入するSQL
INSERT INTO users (user_name, user_id, count_books)
VALUES
  ('田中太郎', '40001', 3),
  ('山田花子', '40002', 1),
  ('佐藤次郎', '40003', 1),
  ('鈴木悠子', '40004', 1),
  ('高橋勇次', '40005', 0),
  ('木村みどり', '40006', 0),
  ('小林宏美', '40007', 0),
  ('渡辺健太', '40008', 0),
  ('山本幸子', '40009', 0),
  ('中村達也', '40010', 0);

-- booksテーブルにダミーデータを挿入するSQL
INSERT INTO books (book_id, book_title, is_borrowed, borrowed_date, return_date, user_id)
VALUES
  ('30021', '世界の中心で、愛をさけぶ', false, NULL, NULL, NULL),
  ('30022', '人間失格', true, '2022-02-01', '2022-02-05', '40001'),
  ('30023', '羊をめぐる冒険', false, NULL, NULL, NULL),
  ('30024', '銀河鉄道の夜', true, '2022-03-01', '2022-03-05', '40002'),
  ('30025', '舟を編む', false, NULL, NULL, NULL),
  ('30026', '蜜蜂と遠雷', true, '2022-03-07', '2022-03-11', '40003'),
  ('30027', '坊っちゃん', true, '2022-02-03', '2022-02-07', '40001'),
  ('30028', '三毛猫ホームズの推理', false, NULL, NULL, NULL),
  ('30029', 'ドグラ・マグラ', true, '2022-02-28', '2022-03-14', '40004'),
  ('30030', '万引き家族', true, '2022-02-03', '2022-02-07', '40001');
  
INSERT INTO staff (id, staff_id, s_pass)
VALUES
  (1, '99999', 'staff'),
  (2, '00000', 'staff');
