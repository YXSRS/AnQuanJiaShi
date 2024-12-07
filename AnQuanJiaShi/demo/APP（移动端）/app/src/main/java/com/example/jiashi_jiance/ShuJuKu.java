package com.example.jiashi_jiance;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;

public class ShuJuKu {
    public static void LianJie_ShuJuKu() {//连接数据库
        /*new Thread(new Runnable() {
            @Override
            public void run() {
                //要连接的数据库url,注意：此处连接的应该是服务器上的MySQl的地址
                String url = "jdbc:mysql://39.103.177.201:3306/anquan_jiashi";//ssmdemo?useSSL=false&serverTimezone=UTC
                //连接数据库使用的用户名
                String userName = "root";
                //连接的数据库时使用的密码
                String password = "gccgcc";
                Connection connection = null;
                try {
                    //1、加载驱动
                    Class.forName("com.mysql.cj.jdbc.Driver");//.newInstance();//com.mysql.cj.jdbc.Driver  com.mysql.jdbc.Driver
                    System.out.println("驱动加载成功！！！");
                } catch (Exception e) {
                    e.printStackTrace();
                }
                try {
                    //2、获取与数据库的连接
                    System.out.println("aaa");
                    connection = DriverManager.getConnection(url, "root", "gccgcc");
                    System.out.println("连接数据库成功！！！");
                    //3.sql语句
                    String sql = "SELECT * FROM anquan_jiashi.zhanghao_biao;";
                    //4.获取用于向数据库发送sql语句的ps
                    PreparedStatement ps = connection.prepareStatement(sql);
                    ps.execute(sql);
                    System.out.println(ps);
                } catch (Exception e) {
                    e.printStackTrace();
                } finally {
                    if (connection != null) {
                        try {
                            connection.close();
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                }
            }
        }).start();
        try {
            Thread.sleep(1000);
        }
        catch (InterruptedException e){
            e.printStackTrace();
        }*/

        //要连接的数据库url,注意：此处连接的应该是服务器上的MySQl的地址
        String url = "jdbc:mysql://39.103.177.201:3306/anquan_jiashi";//ssmdemo?useSSL=false&serverTimezone=UTC
        //连接数据库使用的用户名
        String userName = "root";
        //连接的数据库时使用的密码
        String password = "gccgcc";
        Connection connection = null;
        try {
            //1、加载驱动
            Class.forName("com.mysql.cj.jdbc.Driver");//.newInstance();//com.mysql.cj.jdbc.Driver  com.mysql.jdbc.Driver
            System.out.println("驱动加载成功！！！");
        } catch (Exception e) {
            e.printStackTrace();
        }
        try {
            //2、获取与数据库的连接
            System.out.println("aaa");
            connection = DriverManager.getConnection("jdbc:mysql://39.103.177.201:3306/anquan_jiashi", "root", "gccgcc");
            //?characterEncoding=UTF-8&useUnicode=true&useSSL=false&tinyInt1isBit=false&allowPublicKeyRetrieval=true&serverTimezone=Asia/Shanghai
            System.out.println("连接数据库成功！！！");
            //3.sql语句
            String sql = "SELECT * FROM anquan_jiashi.zhanghao_biao;";
            //4.获取用于向数据库发送sql语句的ps
            PreparedStatement ps = connection.prepareStatement(sql);
            ps.execute(sql);
            System.out.println(ps);

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (connection != null) {
                try {
                    connection.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }

    }
}
