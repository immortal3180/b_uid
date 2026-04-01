# B站UID批量查询工具

一个简单的B站UID批量查询工具，支持按等级筛选和导出。

## 功能特性

- 📋 **列表输入** - 手动输入UID列表（换行或逗号分隔）
- 🔢 **范围查询** - 自动查询指定范围内的所有UID
- 🎯 **等级筛选** - 可勾选要查询的用户等级（0-6级）
- 💾 **导出功能** - 支持导出选中的UID
- 🍪 **Cookie管理** - 支持保存和加载B站Cookie

## 使用方法

### 1. 启动服务

```bash
python server.py
```

### 2. 打开页面

在浏览器中访问：`http://localhost:8888/`

### 3. 设置Cookie（可选）

1. 打开 https://www.bilibili.com/ 并登录
2. 按 `F12` 打开开发者工具
3. 切换到 `Console（控制台）` 标签
4. 输入 `document.cookie` 然后回车
5. 复制输出的内容
6. 粘贴到页面的Cookie文本框
7. 点击"保存Cookie"

### 4. 查询UID

**方式一：列表输入**
- 在文本框中输入UID，每行一个或用逗号分隔

**方式二：范围查询**
- 输入起始UID和结束UID
- 系统会自动查询这个范围内的所有UID

### 5. 筛选和导出

- 勾选你想要的用户等级
- 查询结果可以勾选后导出

## 文件说明

- `server.py` - Python后端服务器
- `index.html` - 前端页面
- `cookie.txt` - Cookie保存文件（不会提交到git）

## 注意事项

- Cookie保存在本地 `cookie.txt` 文件中
- 请不要将 `cookie.txt` 上传到公开仓库
- 查询频率过高可能会被B站限制

## API接口

### 查询用户信息
```
GET /api/bilibili?uid=12345678
```

### 获取当前Cookie
```
GET /api/cookie/get
```

### 保存Cookie
```
POST /api/cookie/save
Content-Type: application/json

{"cookie": "你的Cookie"}
```

## 许可证

MIT
