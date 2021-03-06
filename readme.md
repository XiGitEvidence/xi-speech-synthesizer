# Add task_ogg
Return voice recording in an .OGG container encoded with OPUS.

---

# 习近平讲话模拟器 Xi Jinping Speech Synthesizer

**深受 [韓國瑜發大財產生器](https://rogeraabbccdd.github.io/Fadacai-Generator/#/) 和 [Trumped](https://trumped.com/) 启发，特此创作。**

**本 API 用于合成习近平讲话音频。发送一段文字（简体，繁体，带数字拼音皆可），即可合成非常“真实”的习近平讲话音频。**

#### [立刻体验](https://dnmkrgi.github.io/xi-speech-demo/)

## 注意事项

**本项目仅供娱乐！请勿用于非法用途！**

**本人对圣上没有意见，亦无任何政治诉求。请勿过度解读！**

**使用本项目有巨大风险！后果自负！后果自负！后果自负！**

> 实际上那些错误执行者，他也是有一本账的，这个账是记在那儿的。一旦他出事了，这个账全给你拉出来了。别看你今天闹得欢，小心今后拉清单，这都得应验的。不要干这种事情。头上三尺有神明，一定要有敬畏之心。

![互联网并非法外之地](lqd.jpg)

## 使用方法

### 创建任务

POST https://xi-speech-synthesizer.herokuapp.com/task

Body

```json
{
	"text":"请输入的文字（1000字以内）。支持简体、繁體 ji2 dai4 sheng1 diao4 pin1 yin1."
}
```

Response

```json
{
    "id": "55892d29-cec6-495f-b2b3-3139534efaac",
    "request_successful": true
}
```

### 查询进度

GET  https://xi-speech-synthesizer.herokuapp.com/progress?id=55892d29-cec6-495f-b2b3-3139534efaac

Response (查询成功)

```json
{
    "request_successful": true,
    "result": {
        "finished": true,
        "progress": 1.0
    }
}
```

Response (查询失败)

```json
{
    "message": "找不到此项目",
    "request_successful": false
}
```

### 获取音频

GET https://xi-speech-synthesizer.herokuapp.com/result?id=55892d29-cec6-495f-b2b3-3139534efaac

**返回的音频文件经过base64编码，方便嵌入网页前端**

Response (获取成功)

```json
{
    "request_successful": true,
    "result": {
        "audio": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA/+OgwAAAAAAAAAAAAEluZm8AAAAPAAAAAwAAB1cAjo6Ojo6Ojo6Ojo6Ojo6Ojo6Ojo6Ojo6Ojo6Ojo6Ojo6Ox8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fHx8fH////////////////////////////////////////////AAAAAExhdmM1OC41NAAAAAAAAAAAAAAAACQCWQAAAAAAAAdXMh1+oQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/44DEAAAAA0gAAAAATEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVX/44LEAAAAA0gAAAAATEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVTEFNRTMuMTAwVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV/+OCxAAAAANIAAAAAExBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVQ==",
        "message": [
            "找不到音节 biang",
            "找不到音节 duang",
            "找不到音节 biu"
        ],
        "synthesis_successful": true
    }
}
```

Response (获取失败)

```json
{
    "message": "找不到此项目",
    "request_successful": false
}
```

### 删除数据

DELETE  https://xi-speech-synthesizer.herokuapp.com/result?id=55892d29-cec6-495f-b2b3-3139534efaac

Response 1

```json
{
    "request_successful": true
}
```

Response 2

```json
{
    "message": "项目已被删除",
    "request_successful": false
}
```

**注意：临时存放在服务器上的音频数据会定时清除。**

## 亲自部署

**请确保 Python 版本在 3.6 以上。**

1. 创建并进入[虚拟环境](https://docs.python.org/zh-cn/3/tutorial/venv.html)

2. 安装 requirements.txt 依赖

   ```bash
   $ pip3 install -r requirements.txt
   ```

3. 安装 [ffmpeg](https://github.com/jiaaro/pydub#getting-ffmpeg-set-up) (用于编码 mp3 文件)

4. 运行 Flask APP

   ```bash
   $ export FLASK_APP=api.py
   $ flask run
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```
   Windows 系统下请运行如下命令：
   ```shell
   set FLASK_APP = api.py
   flask run
   ```

## 后话

本人才疏学浅，在本 API 设计上难免有诸多瑕疵和不规范的地方。欢迎各位开 Issue 提供宝贵建议。本人也会认真阅读及采纳 Pull Request。

感谢 YouTube 频道”[乳透社](https://www.youtube.com/c/%E4%B9%B3%E9%80%8F%E7%A4%BE-%E5%B0%8F%E5%8F%8D%E6%97%97/videos)“ 提供的[音源](https://t.co/Pd2UPXozwz?amp=1)。

最后，祝你在奔赴刑场的道路上越走越远！🐻
