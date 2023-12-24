CREATE OR REPLACE FUNCTION manage_blog_posts(
    operation_type VARCHAR, -- Assuming actions include: 'add_post',
                            -- 'get_post', 'update_post', 'delete_post',
                            -- 'add_comment', 'delete_comment', 'get_post_data'
    post_id INT DEFAULT NULL,
    user_id INT DEFAULT NULL,
    post_title VARCHAR DEFAULT NULL,
    post_content TEXT DEFAULT NULL,
    comment_id INT DEFAULT NULL,
    comment_content TEXT DEFAULT NULL,
)
LANGUAGE plpgsql;
RETURNS VOID
AS $$
BEGIN
    CASE operation_type
        WHEN 'add_post' THEN
            -- Add new post
            IF title IS NULL OR user_id IS NULL THEN
                RAISE EXCEPTION 'Title and user_id are required for adding a post';
            END IF;
            INSERT INTO posts (user_id, title, content, created_at)
            VALUES (user_id, post_title, post_content, NOW());

        WHEN 'get_post' THEN
            -- Retrieve post details
            IF post_id IS NOT NULL THEN
                SELECT * FROM posts WHERE id = post_id;
            ELSE
                SELECT * FROM posts
            END IF;

        WHEN 'update_post' THEN
            -- Update post
            IF post_id IS NULL THEN
                RAISE EXCEPTION 'post_id is required for update a post';
            END IF;
            UPDATE posts SET
                title = post_title,
                content = post_content,
                updated_at = NOW()
            WHERE id = post_id;

        WHEN 'delete_post' THEN
            IF post_id IS NULL THEN
                RAISE EXCEPTION 'post_id is required for delete a post';
            END IF;
            -- Delete post
            DELETE FROM posts WHERE id = post_id;

        WHEN 'add_comment' THEN
            IF post_id IS NULL OR user_id IS NULL THEN
                RAISE EXCEPTION 'post_id and user_id are required for adding a comment';
            END IF;
            -- Add comment to post
            INSERT INTO comments (user_id, post_id, content, created_at)
            VALUES (user_id, post_id, comment_content, NOW());

        WHEN 'delete_comment' THEN
            IF comment_id IS NULL THEN
                RAISE EXCEPTION 'comment_id is required for deleting a comment';
            END IF;
            -- Delete comment
            DELETE FROM comments WHERE id = comment_id;

        WHEN 'get_post_data' THEN
            IF post_id IS NULL THEN
                RAISE EXCEPTION 'post_id is required for fetching post data';
            END IF;
            -- Fetch post-related data (comments)
            SELECT
                p.id AS post_id,
                p.title AS post_title,
                p.content AS post_content,
                c.id AS comment_id,
                c.content AS comment_content
            FROM posts p
            LEFT JOIN comments c ON p.id = c.post_id
            WHERE p.id = post_id;

        ELSE
            -- Handle unknown operation type
            RAISE EXCEPTION 'Invalid operation type: %', operation_type;

    END CASE;
END;
$$
