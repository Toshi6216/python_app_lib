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
  isbn VARCHAR(20) NOT NULL,
  book_title VARCHAR(40) NOT NULL,
  is_borrowed BOOLEAN NOT NULL,
  borrowed_date DATE,
  return_date DATE,
  user_id VARCHAR(255),
  count_borrowed int not null,
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
INSERT INTO books (book_id, isbn, book_title, is_borrowed, borrowed_date, return_date, user_id, count_borrowed)
VALUES
  ('30021', '9784087746637', '世界の中心で、愛をさけぶ', false, NULL, NULL, NULL, 10),
  ('30022', '9784001155217', '人間失格', true, '2022-02-01', '2022-02-05', '40001', 6),
  ('30023', '9784048739022', '羊をめぐる冒険', false, NULL, NULL, NULL, 6),
  ('30024', '9784046213986', '銀河鉄道の夜', true, '2022-03-01', '2022-03-05', '40002', 4),
  ('30025', '9784061851109', '舟を編む', false, NULL, NULL, NULL, 0),
  ('30026', '9784167119024', '蜜蜂と遠雷', true, '2022-03-07', '2022-03-11', '40003', 5),
  ('30027', '9784087712441', '坊っちゃん', true, '2022-02-03', '2022-02-07', '40001', 8),
  ('30028', '9784062932558', '三毛猫ホームズの推理', false, NULL, NULL, NULL, 1),
  ('30029', '9784101000019', 'ドグラ・マグラ', true, '2022-02-28', '2022-03-14', '40004', 2),
  ('30030', '9784062936365', '万引き家族', true, '2022-02-03', '2022-02-07', '40001', 4),
  ('30031', '9784087746637', '世界の中心で、愛をさけぶ', false, NULL, NULL, NULL, 8),
  ('30032', '9784087746637', '世界の中心で、愛をさけぶ', false, NULL, NULL, NULL, 5);


  
INSERT INTO staff (id, staff_id, s_pass)
VALUES
  (1, '99999', 'staff'),
  (2, '00000', 'staff');
