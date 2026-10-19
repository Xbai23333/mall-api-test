
-- 为 CI 专用管理员分配超级管理员角色
-- 此脚本应在管理员注册成功后执行

INSERT INTO ums_admin_role_relation (admin_id, role_id)
SELECT a.id, 5
FROM ums_admin AS a
WHERE a.username = 'mall_ci_admin'
  AND NOT EXISTS (
    SELECT 1
    FROM ums_admin_role_relation AS r
    WHERE r.admin_id = a.id
      AND r.role_id = 5
  );
