
QUERIES = {'categories': 'SELECT category_id, name FROM category ORDER BY name',
 'search': 'SELECT b.book_id, b.title, b.price, b.publish_year, a.name AS author, c.name AS '
           'category\n'
           'FROM book b JOIN author a ON b.author_id = a.author_id\n'
           'JOIN category c ON b.category_id = c.category_id\n'
           'WHERE b.title LIKE %s AND b.price BETWEEN %s AND %s\n'
           '  AND (%s IS NULL OR b.category_id = %s)\n'
           'ORDER BY b.price ASC, b.book_id ASC',
 'catalogue': 'SELECT b.book_id, b.title, b.price, b.publish_year,\n'
              '       a.name AS author, p.name AS publisher, c.name AS category\n'
              'FROM book b JOIN author a ON b.author_id = a.author_id\n'
              'JOIN publisher p ON b.publisher_id = p.publisher_id\n'
              'JOIN category c ON b.category_id = c.category_id\n'
              'ORDER BY b.title, b.book_id',
 'category_report': 'SELECT c.name AS category, COUNT(b.book_id) AS book_count, '
                    'ROUND(AVG(b.price), 2) AS average_price\n'
                    'FROM category c LEFT JOIN book b ON c.category_id = b.category_id\n'
                    'GROUP BY c.category_id, c.name ORDER BY c.name',
 'prolific_authors': 'SELECT a.name AS author, COUNT(b.book_id) AS book_count\n'
                     'FROM author a JOIN book b ON a.author_id = b.author_id\n'
                     'GROUP BY a.author_id, a.name HAVING COUNT(b.book_id) >= 2\n'
                     'ORDER BY book_count DESC, a.author_id',
 'price_summary': 'SELECT SUM(price) AS total_price, MIN(price) AS smallest_price, MAX(price) AS '
                  'largest_price FROM book',
 'active_loans': 'SELECT l.loan_id, b.title AS book, m.name AS member, l.loan_date\n'
                 'FROM loan l JOIN book b ON l.book_id = b.book_id\n'
                 'JOIN member m ON l.member_id = m.member_id\n'
                 'WHERE l.return_date IS NULL ORDER BY l.loan_date, l.loan_id',
 'never_members': 'SELECT m.member_id, m.name, m.email FROM member m\n'
                  'LEFT JOIN loan l ON m.member_id = l.member_id\n'
                  'WHERE l.loan_id IS NULL ORDER BY m.member_id',
 'never_books': 'SELECT b.book_id, b.title FROM book b\n'
                'LEFT JOIN loan l ON b.book_id = l.book_id\n'
                'WHERE l.loan_id IS NULL ORDER BY b.book_id',
 'top_books': 'SELECT b.book_id, b.title, COUNT(l.loan_id) AS loan_count\n'
              'FROM book b JOIN loan l ON b.book_id = l.book_id\n'
              'GROUP BY b.book_id, b.title ORDER BY loan_count DESC, b.book_id ASC LIMIT 3',
 'top_member': 'SELECT m.member_id, m.name AS member, COUNT(l.loan_id) AS loan_count\n'
               'FROM member m JOIN loan l ON m.member_id = l.member_id\n'
               'GROUP BY m.member_id, m.name ORDER BY loan_count DESC, m.member_id ASC LIMIT 1',
 'author_counts': 'SELECT a.name AS author, a.country, COUNT(b.book_id) AS book_count\n'
                  'FROM author a LEFT JOIN book b ON a.author_id = b.author_id\n'
                  'GROUP BY a.author_id, a.name, a.country ORDER BY a.author_id',
 'same_country': 'SELECT b.title, a.name AS author, p.name AS publisher, a.country\n'
                 'FROM book b JOIN author a ON b.author_id = a.author_id\n'
                 'JOIN publisher p ON b.publisher_id = p.publisher_id\n'
                 'WHERE a.country = p.country ORDER BY b.book_id'}

LAB5_QUERIES = {'above_average': 'SELECT bd.title, bd.price,\n'
                  '       ROUND((SELECT AVG(price) FROM book), 2) AS library_average_price\n'
                  'FROM book_details bd\n'
                  'WHERE bd.price > (SELECT AVG(price) FROM book)\n'
                  'ORDER BY bd.price DESC, bd.book_id',
 'never_borrowed_books': 'SELECT b.book_id, b.title\n'
                         'FROM book b\n'
                         'WHERE NOT EXISTS (SELECT * FROM loan l WHERE l.book_id = b.book_id)\n'
                         'ORDER BY b.book_id',
 'never_borrowed_members': 'SELECT m.member_id, m.name, m.email\n'
                           'FROM member m\n'
                           'WHERE NOT EXISTS (SELECT * FROM loan l WHERE l.member_id = '
                           'm.member_id)\n'
                           'ORDER BY m.member_id',
 'category_most_expensive': 'SELECT bd.category, bd.title, bd.price\n'
                            'FROM book_details bd\n'
                            'WHERE bd.price = (SELECT MAX(b.price) FROM book b WHERE b.category_id '
                            '= bd.category_id)\n'
                            'ORDER BY bd.category, bd.title, bd.book_id',
 'category_above_average': 'SELECT bd.category, bd.title, bd.price,\n'
                           '       ROUND((SELECT AVG(b.price) FROM book b WHERE b.category_id = '
                           'bd.category_id), 2) AS category_average_price\n'
                           'FROM book_details bd\n'
                           'WHERE bd.price > (SELECT AVG(b.price) FROM book b WHERE b.category_id '
                           '= bd.category_id)\n'
                           'ORDER BY bd.category, bd.price DESC, bd.book_id',
 'average_member_loans': 'SELECT ROUND(AVG(member_loans.loan_count), 2) AS '
                         'average_loans_per_member\n'
                         'FROM (\n'
                         '    SELECT m.member_id, COUNT(l.loan_id) AS loan_count\n'
                         '    FROM member m LEFT JOIN loan l ON l.member_id = m.member_id\n'
                         '    GROUP BY m.member_id\n'
                         ') AS member_loans',
 'active_members': 'SELECT m.member_id, m.name AS member, COUNT(l.loan_id) AS loan_count\n'
                   'FROM member m LEFT JOIN loan l ON l.member_id = m.member_id\n'
                   'GROUP BY m.member_id, m.name\n'
                   'HAVING COUNT(l.loan_id) > (\n'
                   '    SELECT AVG(member_loans.loan_count)\n'
                   '    FROM (\n'
                   '        SELECT m2.member_id, COUNT(l2.loan_id) AS loan_count\n'
                   '        FROM member m2 LEFT JOIN loan l2 ON l2.member_id = m2.member_id\n'
                   '        GROUP BY m2.member_id\n'
                   '    ) AS member_loans\n'
                   ')\n'
                   'ORDER BY loan_count DESC, m.member_id',
 'borrowed_authors': 'SELECT a.author_id, a.name AS author, a.country\n'
                     'FROM author a\n'
                     'WHERE EXISTS (\n'
                     '    SELECT * FROM book b JOIN loan l ON l.book_id = b.book_id\n'
                     '    WHERE b.author_id = a.author_id\n'
                     ')\n'
                     'ORDER BY a.name, a.author_id',
 'review_summary': 'SELECT b.title, COUNT(r.review_id) AS review_count,\n'
                   '       COALESCE(ROUND(AVG(r.rating), 2), 0) AS average_rating,\n'
                   '       CASE\n'
                   "           WHEN COUNT(r.review_id) = 0 THEN 'No review'\n"
                   "           WHEN AVG(r.rating) >= 4.5 THEN 'Excellent'\n"
                   "           WHEN AVG(r.rating) >= 3.5 THEN 'Good'\n"
                   "           ELSE 'Fair'\n"
                   '       END AS rating_label\n'
                   'FROM book b LEFT JOIN review r ON r.book_id = b.book_id\n'
                   'GROUP BY b.book_id, b.title\n'
                   'ORDER BY b.title, b.book_id',
 'above_average_reviews': 'SELECT b.title, COUNT(r.review_id) AS review_count,\n'
                          '       ROUND(AVG(r.rating), 2) AS average_rating,\n'
                          '       ROUND((SELECT AVG(rating) FROM review), 2) AS '
                          'overall_average_rating\n'
                          'FROM book b JOIN review r ON r.book_id = b.book_id\n'
                          'GROUP BY b.book_id, b.title\n'
                          'HAVING AVG(r.rating) > (SELECT AVG(rating) FROM review)\n'
                          'ORDER BY average_rating DESC, b.book_id',
 'all_countries': 'SELECT country FROM author\n'
                  'UNION\n'
                  'SELECT country FROM publisher\n'
                  'ORDER BY country',
 'shared_countries': 'SELECT country FROM author\n'
                     'INTERSECT\n'
                     'SELECT country FROM publisher\n'
                     'ORDER BY country',
 'author_only_countries': 'SELECT country FROM author\n'
                          'EXCEPT\n'
                          'SELECT country FROM publisher\n'
                          'ORDER BY country',
 'people': "SELECT name, 'Author' AS type FROM author\n"
           'UNION ALL\n'
           "SELECT name, 'Member' AS type FROM member\n"
           'ORDER BY name, type'}
