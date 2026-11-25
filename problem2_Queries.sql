USE library;

SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;

-- F2.1
SELECT bd.title, bd.price,
       ROUND((SELECT AVG(price) FROM book), 2) AS library_average_price
FROM book_details bd
WHERE bd.price > (SELECT AVG(price) FROM book)
ORDER BY bd.price DESC, bd.book_id;

-- F2.2
SELECT b.book_id, b.title
FROM book b
WHERE NOT EXISTS (SELECT * FROM loan l WHERE l.book_id = b.book_id)
ORDER BY b.book_id;

-- F2.2
SELECT m.member_id, m.name, m.email
FROM member m
WHERE NOT EXISTS (SELECT * FROM loan l WHERE l.member_id = m.member_id)
ORDER BY m.member_id;

-- F2.3
SELECT bd.category, bd.title, bd.price
FROM book_details bd
WHERE bd.price = (SELECT MAX(b.price) FROM book b WHERE b.category_id = bd.category_id)
ORDER BY bd.category, bd.title, bd.book_id;

-- F2.3
SELECT bd.category, bd.title, bd.price,
       ROUND((SELECT AVG(b.price) FROM book b WHERE b.category_id = bd.category_id), 2) AS category_average_price
FROM book_details bd
WHERE bd.price > (SELECT AVG(b.price) FROM book b WHERE b.category_id = bd.category_id)
ORDER BY bd.category, bd.price DESC, bd.book_id;

-- F2.4
SELECT ROUND(AVG(member_loans.loan_count), 2) AS average_loans_per_member
FROM (
    SELECT m.member_id, COUNT(l.loan_id) AS loan_count
    FROM member m LEFT JOIN loan l ON l.member_id = m.member_id
    GROUP BY m.member_id
) AS member_loans;

-- F2.4
SELECT m.member_id, m.name AS member, COUNT(l.loan_id) AS loan_count
FROM member m LEFT JOIN loan l ON l.member_id = m.member_id
GROUP BY m.member_id, m.name
HAVING COUNT(l.loan_id) > (
    SELECT AVG(member_loans.loan_count)
    FROM (
        SELECT m2.member_id, COUNT(l2.loan_id) AS loan_count
        FROM member m2 LEFT JOIN loan l2 ON l2.member_id = m2.member_id
        GROUP BY m2.member_id
    ) AS member_loans
)
ORDER BY loan_count DESC, m.member_id;

-- F2.4
SELECT a.author_id, a.name AS author, a.country
FROM author a
WHERE EXISTS (
    SELECT * FROM book b JOIN loan l ON l.book_id = b.book_id
    WHERE b.author_id = a.author_id
)
ORDER BY a.name, a.author_id;

-- F2.5
SELECT b.title, COUNT(r.review_id) AS review_count,
       COALESCE(ROUND(AVG(r.rating), 2), 0) AS average_rating,
       CASE
           WHEN COUNT(r.review_id) = 0 THEN 'No review'
           WHEN AVG(r.rating) >= 4.5 THEN 'Excellent'
           WHEN AVG(r.rating) >= 3.5 THEN 'Good'
           ELSE 'Fair'
       END AS rating_label
FROM book b LEFT JOIN review r ON r.book_id = b.book_id
GROUP BY b.book_id, b.title
ORDER BY b.title, b.book_id;

-- F2.5
SELECT b.title, COUNT(r.review_id) AS review_count,
       ROUND(AVG(r.rating), 2) AS average_rating,
       ROUND((SELECT AVG(rating) FROM review), 2) AS overall_average_rating
FROM book b JOIN review r ON r.book_id = b.book_id
GROUP BY b.book_id, b.title
HAVING AVG(r.rating) > (SELECT AVG(rating) FROM review)
ORDER BY average_rating DESC, b.book_id;

-- F2.6
SELECT country FROM author
UNION
SELECT country FROM publisher
ORDER BY country;

-- F2.6
SELECT country FROM author
INTERSECT
SELECT country FROM publisher
ORDER BY country;

-- F2.6
SELECT country FROM author
EXCEPT
SELECT country FROM publisher
ORDER BY country;

-- F2.6
SELECT name, 'Author' AS type FROM author
UNION ALL
SELECT name, 'Member' AS type FROM member
ORDER BY name, type;
