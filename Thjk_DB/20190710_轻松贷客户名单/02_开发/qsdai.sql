-- 正则替换掉注释      (?:^|[ ]+)(?:#|--) +[^\n]*
SELECT
    merchant_ap                         as `商户号`         -- 商户号
    ,aaa.inst_name                      as `机构名称`       -- 机构名称
    ,merchant_zc.aip_bran_id              as `机构代码`       -- 机构代码
    ,merchant_zc.area_cd                  as `地区码`        -- 合成地区码
    ,dim_area.area_name                  as `地区名称`       -- 地区名称
    ,merchant_zc.prov_cd          as `省份码`        -- 省份码
    ,merchant_zc.city_cd          as `城市码`        -- 城市码
    ,merchant_zc.area_cd       as `区县码`        -- 区县码
    ,merchant_zc.legal_name    as `法人姓名`       -- 法人姓名
--    ,upper(regexp_replace(merchant_zc.legal_iden_no,'\\s','')) as `身份证`  -- 身份证号码去空格大写
    ,merchant_zc.name            as `商户名称`               -- 商户名称
    ,merchant_zc.contact_tel        as `联系电话`               -- 联系电话
    ,fff.bl_login_mobile                as `好老板登录手机`         -- 保理登录手机
    ,fff.bl_bank_mobile_phone           as `好老板银行手机`         -- 保理银行手机
    ,fff.zc_login_mobile                as `通联宝登录手机`         -- 资产登录手机
    ,fff.zc_bank_mobile_phone           as `通联宝银行手机`         -- 资产银行手机
    --  ,merchant_info.*
from dm_2g.dm_qsd_merchant               -- 商户号，年龄范围，流水额度
LEFT JOIN rds_rc.merchant_zc         -- 商户基础信息表
on dm_qsd_merchant.merchant_ap=merchant_zc.mcht_cd           -- 商户号相等
LEFT JOIN dim.dim_area           -- 地区表
on merchant_zc.area_cd = dim_area.area_no                 -- 地区编码一致
LEFT JOIN
(                               -- 机构名称表
    SELECT inst_name,bran_cd            -- 机构名称，机构编号
    from
    rds_rc.organization                 -- 机构表
    where bran_cd LIKE '99%'            -- 99 开头才是分公司
        and inst_name like '%分公司'
) aaa
on merchant_zc.aip_bran_id = aaa.bran_cd  -- 机构编号相等
left join
(                               -- 资产保理注册用户手机号码
    SELECT
        coalesce(bbb.legal_id_no,ddd.legal_id_no) as legal_id_no,   -- 保理资产有一个有数据就可以
        bbb.login_mobile as bl_login_mobile,                        -- 保理登录手机
        bbb.bank_mobile_phone as bl_bank_mobile_phone,              -- 保理银行手机
        ddd.login_mobile as zc_login_mobile,                        -- 资产登录手机
        ddd.bank_mobile_phone as zc_bank_mobile_phone               -- 资产银行手机
    from
    (                           -- 保理手机号码表
        SELECT
            login_mobile                                            -- 登录手机号
            ,bank_mobile_phone                                      -- 银行手机号
            ,id_no as legal_id_no                                   -- 法人身份证
        from
        (
            SELECT
                login_mobile,bank_mobile_phone
                ,upper(regexp_replace(legal_id_no,'\\s',''))        -- 身份证号码去空格大写
                as id_no
                ,( row_number() over (PARTITION BY user.legal_id_no ORDER BY user.last_update_time desc ) )
                as row_num                                          -- 有多个记录，只要最新的一个
            from rds_rc.`user`
            where source=1                                          -- 保理系统
        ) aaa
        where row_num = 1 and length(id_no)>=18                     -- 有多个记录，只要最新的一个
    ) bbb
    full join
    (                           -- 资产手机号码表
        SELECT
            login_mobile                                            -- 登录手机号
            ,bank_mobile_phone                                      -- 银行手机号
            ,id_no as legal_id_no                                   -- 法人身份证
        from
        (
            SELECT
                login_mobile,bank_mobile_phone
                ,upper(regexp_replace(legal_id_no,'\\s',''))        -- 身份证号码去空格大写
                as id_no
                ,( row_number() over (PARTITION BY user.legal_id_no ORDER BY user.last_update_time desc ) )
                as row_num                                          -- 有多个记录，只要最新的一个
            from rds_rc.`user`
            where source=2                                          -- 资产系统
        ) ccc
        where row_num = 1 and length(id_no)>=18                     -- 有多个记录，只要最新的一个
    ) ddd
    on bbb.legal_id_no = ddd.legal_id_no                            -- 用身份证号码关联
 ) fff
 on upper(regexp_replace(merchant_zc.legal_iden_no,'\\s','')) = fff.legal_id_no  -- 用身份证号码关联
order by
    `机构名称` desc
    ,`地区名称`
    ,`法人姓名`


