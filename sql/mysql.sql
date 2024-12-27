-- 用户账户表
CREATE TABLE t_user_accounts
(
    id                 BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '账户ID',
    username           VARCHAR(50)    NOT NULL UNIQUE COMMENT '用户名',
    email              VARCHAR(100)   NOT NULL DEFAULT '' UNIQUE COMMENT '电子邮件',
    phone_country_code VARCHAR(10)    NOT NULL DEFAULT '86' UNIQUE COMMENT '国家编码',
    phone              VARCHAR(20)    NOT NULL DEFAULT '' UNIQUE COMMENT '手机号',
    nickname           VARCHAR(50)    NOT NULL DEFAULT '' COMMENT '昵称',
    avatar             VARCHAR(255)   NOT NULL DEFAULT '' COMMENT '头像URL',
    password_hash      VARCHAR(255)   NOT NULL DEFAULT '' COMMENT '密码哈希值',
    salt               VARCHAR(32)    NOT NULL DEFAULT '' COMMENT '密码盐',
    balance            DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT '账户余额',
    points             INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '积分',
    frozen_amount      DECIMAL(10, 2) NOT NULL DEFAULT 0.00 COMMENT '冻结金额',
    status             TINYINT(1) NOT NULL DEFAULT 1 COMMENT '状态 (1:正常, 0:禁用)',
    created_at         DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at         DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户账户表';

-- 用户交易记录表
CREATE TABLE t_user_transactions
(
    id               BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '交易ID',
    user_id          BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    transaction_type TINYINT(1) NOT NULL COMMENT '类型 (1:收入, 2:支出, 3:冻结, 4:解冻)',
    amount           DECIMAL(10, 2) NOT NULL COMMENT '交易金额',
    balance_before   DECIMAL(10, 2) NOT NULL COMMENT '交易前余额',
    balance_after    DECIMAL(10, 2) NOT NULL COMMENT '交易后余额',
    transaction_type TINYINT        NOT NULL COMMENT '交易类型(1:充值, 2:消费, 3:提现)',
    remark           VARCHAR(255)   NOT NULL DEFAULT '' COMMENT '备注',
    created_at       DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '交易时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户交易记录表';

-- 用户提现表
CREATE TABLE t_user_withdrawals
(
    id           BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '提现ID',
    user_id      BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    amount       DECIMAL(10, 2) NOT NULL COMMENT '提现金额',
    bank_account VARCHAR(100)   NOT NULL COMMENT '提现银行卡号',
    bank_name    VARCHAR(50)    NOT NULL COMMENT '银行名称',
    status       TINYINT(1) NOT NULL DEFAULT 0 COMMENT '状态 (0:待审核, 1:已完成, 2:拒绝)',
    reviewer     VARCHAR(50)    NOT NULL DEFAULT '' COMMENT '审核人',
    remark       VARCHAR(255)   NOT NULL DEFAULT '' COMMENT '备注',
    created_at   DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '提现申请时间',
    updated_at   DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户提现表';

-- 用户充值表
CREATE TABLE t_user_recharges
(
    id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '充值ID',
    user_id           BIGINT UNSIGNED NOT NULL COMMENT '用户ID',
    amount            DECIMAL(10, 2) NOT NULL COMMENT '充值金额',
    payment_method    VARCHAR(50)    NOT NULL COMMENT '支付方式',
    original_currency VARCHAR(10)    NOT NULL COMMENT '原始充值币种',
    exchange_rate     DECIMAL(10, 6) NOT NULL COMMENT '充值时汇率',
    status            TINYINT(1) NOT NULL DEFAULT 0 COMMENT '状态 (0:待支付, 1:已完成, 2:失败)',
    reviewer          VARCHAR(50)    NOT NULL DEFAULT '' COMMENT '审核人',
    remark            VARCHAR(255)   NOT NULL DEFAULT '' COMMENT '备注',
    created_at        DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '充值申请时间',
    updated_at        DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户充值表';

-- 外键约束示例
ALTER TABLE t_user_accounts
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES t_users (id) ON DELETE CASCADE;
ALTER TABLE t_user_transactions
    ADD CONSTRAINT fk_transaction_user_id FOREIGN KEY (user_id) REFERENCES t_users (id) ON DELETE CASCADE;
ALTER TABLE t_user_withdrawals
    ADD CONSTRAINT fk_withdrawal_user_id FOREIGN KEY (user_id) REFERENCES t_users (id) ON DELETE CASCADE;
ALTER TABLE t_user_recharges
    ADD CONSTRAINT fk_recharge_user_id FOREIGN KEY (user_id) REFERENCES t_users (id) ON DELETE CASCADE;


-- 订单表 (service_order)
CREATE TABLE t_orders
(
    id           BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '订单ID',
    user_id      BIGINT         NOT NULL COMMENT '用户ID',
    total_amount DECIMAL(10, 2) NOT NULL COMMENT '订单总金额',
    status       TINYINT   DEFAULT 0 COMMENT '订单状态(0:待支付, 1:已支付, 2:已取消)',
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES t_users (id) ON DELETE CASCADE
);

-- 订单详情表
CREATE TABLE t_order_details
(
    id          BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '订单详情ID',
    order_id    BIGINT         NOT NULL COMMENT '订单ID',
    product_id  BIGINT         NOT NULL COMMENT '产品ID',
    quantity    INT            NOT NULL COMMENT '数量',
    price       DECIMAL(10, 2) NOT NULL COMMENT '单价',
    total_price DECIMAL(10, 2) NOT NULL COMMENT '总价',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (order_id) REFERENCES t_orders (id) ON DELETE CASCADE
);

-- 产品表 (service_product)
CREATE TABLE t_products
(
    id          BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '产品ID',
    name        VARCHAR(100)   NOT NULL COMMENT '产品名称',
    description TEXT COMMENT '产品描述',
    price       DECIMAL(10, 2) NOT NULL COMMENT '价格',
    stock       INT       DEFAULT 0 COMMENT '库存数量',
    status      TINYINT   DEFAULT 1 COMMENT '状态(1:上架, 0:下架)',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
);

-- 库存表
CREATE TABLE t_inventory
(
    id         BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '库存ID',
    product_id BIGINT NOT NULL COMMENT '产品ID',
    quantity   INT       DEFAULT 0 COMMENT '库存数量',
    reserved   INT       DEFAULT 0 COMMENT '预留库存',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (product_id) REFERENCES t_products (id) ON DELETE CASCADE
);


-- 昵称表
CREATE TABLE `t_nicknames`
(
    `id`          int                                                           NOT NULL AUTO_INCREMENT,
    `nickname`    varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    `usage_count` int                                                           NOT NULL DEFAULT '0',
    `deleted`     tinyint                                                       NOT NULL DEFAULT '0',
    `create_time` datetime                                                      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `update_time` datetime                                                      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `nickname` (`nickname`)
) ENGINE=InnoDB AUTO_INCREMENT=16772 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;