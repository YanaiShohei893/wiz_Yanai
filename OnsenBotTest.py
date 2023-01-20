from flask import Flask, request, abort
import os
import psycopg2
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    ButtonsTemplate, CarouselColumn, CarouselTemplate, 
    BubbleContainer, CarouselContainer, BoxComponent, TextComponent, ButtonComponent,
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, FlexSendMessage,
    PostbackAction, PostbackTemplateAction
)

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# Pythonでは呼び出す行より上に記述しないとエラーになる

# ブラウザでアクセスした場合の処理
@app.route("/")
def hello_world():
    return "hello world!"

# LINEからメッセージを受け取った場合の処理
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        # 署名を検証し、問題なければhandleに定義されている関数を呼び出す
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# フォローイベントの場合の処理
@handler.add(FollowEvent)
def handle_follow(event):
    profile = line_bot_api.get_profile(event.source.user_id)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=profile.display_name + "さん、はじめまして！\n" +
        "友だち追加ありがとうございます。福島温泉情報bot（仮）です。\n" +
        "温泉の情報を探したい場合は、まずは「温泉を探す」をタップしてください。")
    )

# メッセージイベントの場合の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    content = event.message.text # メッセージの内容を取得する
    if content in ['温泉を探す']:
        carousel_columns = [
            CarouselColumn(
                text='希望する地方を選択してください',
                title='会津で検索',
                actions=[
                    PostbackTemplateAction(
                        label='会津',
                        data='callback',
                        text='会津'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する地方を選択してください',
                title='中通りで検索',
                actions=[
                    PostbackTemplateAction(
                        label='中通り',
                        data='callback',
                        text='中通り'
                    )
                ]
            ),
            CarouselColumn(
                text='希望する地方を選択してください',
                title='浜通りで検索',
                actions=[
                    PostbackTemplateAction(
                        label='浜通り',
                        data='callback',
                        text='浜通り'
                    )
                ]
            ),
            CarouselColumn(
                text='希望する地方を選択してください',
                title='希望なし',
                actions=[
                    PostbackTemplateAction(
                        label='場所なし',
                        data='callback',
                        text='場所なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )

    elif content in ['会津']:
        carousel_columns = [
            CarouselColumn(
                text='希望する景色を選択してください',
                title='景色で検索',
                actions=[
                    PostbackTemplateAction(
                        label='雪景色',
                        data='callback',
                        text='会津.雪景色'   
                    ),
                    PostbackTemplateAction(
                        label='紅葉',
                        data='callback',
                        text='会津.紅葉'   
                    ),
                    PostbackTemplateAction(
                        label='夜空',
                        data='callback',
                        text='会津.夜空'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する景色を選択してください',
                title='景色で検索',
                actions=[
                     PostbackTemplateAction(
                        label='川 or 海',
                        data='callback',
                        text='会津.川 or 海'   
                    ),
                     PostbackTemplateAction(
                        label='森',
                        data='callback',
                        text='会津.森'   
                    ),
                     PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='会津.景色なし'   
                    )        
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
    
    elif content in ['会津.雪景色']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='会津.雪景色.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='会津.雪景色.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='会津.雪景色.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                     PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='会津.雪景色.生活習慣病'   
                    ),
                     PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='会津.雪景色.皮膚病'   
                    ),
                     PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='会津.雪景色.効能なし'   
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
        
    elif content in ['会津.紅葉']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='会津.紅葉.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='会津.紅葉.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='会津.紅葉.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                     PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='会津.紅葉.生活習慣病'   
                    ),
                     PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='会津.紅葉.皮膚病'   
                    ),
                     PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='会津.紅葉.効能なし'   
                    )
                    
                ]
            )
            
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
        
    elif content in ['会津.夜空']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='会津.夜空.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='会津.夜空.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='会津.夜空.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                     PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='会津.夜空.生活習慣病'   
                    ),
                     PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='会津.夜空.皮膚病'   
                    ),
                     PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='会津.夜空.効能なし'   
                    )
                ]
            )  
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
        
     #「会津.川 or 海」に対しての返信 「求める効能」について質問する
    elif content in ['会津.川 or 海']:
        
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='会津.川 or 海.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='会津.川 or 海.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='会津.川 or 海.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                     PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='会津.川 or 海.生活習慣病'   
                    ),
                     PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='会津.川 or 海.皮膚病'   
                    ),
                     PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='会津.川 or 海.効能なし'   
                    )
                    
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
        
    elif content in ['会津.森']:
        
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='会津.森.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='会津.森.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='会津.森.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                     PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='会津.森.生活習慣病'   
                    ),
                     PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='会津.森.皮膚病'   
                    ),
                     PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='会津.森.効能なし'   
                    )
                    
                ]
            )
            
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
        
    #「会津.景色なし」に対しての返信 「求める効能」について質問する
    elif content in ['会津.景色なし']:
        
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='会津.景色なし.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='会津.景色なし.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='会津.景色なし.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                     PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='会津.景色なし.生活習慣病'   
                    ),
                     PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='会津.景色なし.皮膚病'   
                    ),
                     PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='会津.景色なし.効能なし'   
                    )
                    
                ]
            )
            
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
        


   

##「浜通り」と受け取った時の処理
    elif content in ['浜通り']:
        carousel_columns = [
            CarouselColumn(
                text='希望する景色を選択してください',
                title='景色で検索',
                actions=[
                    PostbackTemplateAction(
                        label='雪景色',
                        data='callback',
                        text='浜通り.雪景色'   
                    ),
                    PostbackTemplateAction(
                        label='紅葉',
                        data='callback',
                        text='浜通り.紅葉'   
                    ),
                    PostbackTemplateAction(
                        label='夜空',
                        data='callback',
                        text='浜通り.夜空'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する景色を選択してください',
                title='景色で検索',
                actions=[
                    PostbackTemplateAction(
                        label='川 or 海',
                        data='callback',
                        text='浜通り.川 or 海'
                    ),
                
                    
                    PostbackTemplateAction(
                        label='森',
                        data='callback',
                        text='浜通り.森'
                    ),
                    
        
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='浜通り.景色なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
    ##「浜通り.雪景色」と受け取った時の処理
    elif content in ['浜通り.雪景色']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='浜通り.雪景色.美肌'   
                    ),
                
                
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='浜通り.雪景色.傷'   
                    ),
                
                
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='浜通り.雪景色.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='浜通り.雪景色.生活習慣病'
                    ),
                
                
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='浜通り.雪景色.皮膚病'
                    ),
                
                
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='浜通り.雪景色.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,  
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
    ##「浜通り.紅葉」と受け取った時の処理
    elif content in ['浜通り.紅葉']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='浜通り.紅葉.美肌'   
                    ),
                
                
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='浜通り.紅葉.傷'   
                    ),
                
                
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='浜通り.紅葉.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='浜通り.紅葉.生活習慣病'
                    ),
                
                
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='浜通り.紅葉.皮膚病'
                    ),
                
                
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='浜通り.紅葉.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,  
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
    ##「浜通り.夜空」と受け取った時の処理
    elif content in ['浜通り.夜空']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='浜通り.夜空.美肌'   
                    ),
                
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='浜通り.夜空.傷'   
                    ),
                
            
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='浜通り.夜空.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='浜通り.夜空.生活習慣病'
                    ),

                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='浜通り.夜空.皮膚病'
                    ),
                    
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='浜通り.夜空.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,  
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
    ##「浜通り.川 or 海」と受け取った時の処理
    elif content in ['浜通り.川 or 海']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='浜通り.川 or 海.美肌'   
                    ),
                    
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='浜通り.川 or 海.傷'   
                    ),
                
                
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='浜通り.川 or 海.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='浜通り.川 or 海.生活習慣病'
                    ),
                
                
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='浜通り.川 or 海.皮膚病'
                    ),
                
                
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='浜通り.川 or 海.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,  
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
    ##「浜通り.森」と受け取った時の処理
    elif content in ['浜通り.森']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='浜通り.森.美肌'   
                    ),
                
                
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='浜通り.森.傷'   
                    ),
                
                
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='浜通り.森.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='浜通り.森.生活習慣病'
                    ),
                
                
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='浜通り.森.皮膚病'
                    ),
                
                
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='浜通り.森.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,  
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
##「浜通り.景色なし」と受け取った時の処理
    elif content in ['浜通り.景色なし']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='浜通り.景色なし.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='浜通り.景色なし.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='浜通り.景色なし.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='浜通り.景色なし.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='浜通り.景色なし.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='浜通り.景色なし.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,  
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )






##中通りと受け取った時の処理
    elif content in ['中通り']:
        carousel_columns = [
            CarouselColumn(
                text='希望する景色を選択してください',
                title='景色で検索',
                actions=[
                    PostbackTemplateAction(
                        ##label='中通り.雪景色',
                        label='雪景色',
                        data='callback',
                        text='中通り.雪景色'   
                    ),
                
                    PostbackTemplateAction(
                        label='紅葉',
                        data='callback',
                        text='中通り.紅葉'   
                    ),
                    PostbackTemplateAction(
                        label='夜空',
                        data='callback',
                        text='中通り.夜空'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する景色を選択してください',
                title='景色で検索',
                actions=[
                    PostbackTemplateAction(
                        label='川 or海',
                        data='callback',
                        text='中通り.川 or 海'
                    ),
                    PostbackTemplateAction(
                        label='森',
                        data='callback',
                        text='中通り.森'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='中通り.景色なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
    )
##中通り.雪景色を受け取った時の処理
    elif content in ['中通り.雪景色']:
        carousel_columns = [
            CarouselColumn(
                text='希望する泉質名を選択してください',
                title='泉質名で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='中通り.雪景色.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='中通り.雪景色.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='中通り.雪景色.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する景色を選択してください',
                title='景色で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='中通り.雪景色.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='中通り.雪景色.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='中通り.雪景色.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
        ##「中通り.紅葉」と受け取った時の処理
    elif content in ['中通り.紅葉']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='中通り.紅葉.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='中通り.紅葉.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='中通り.紅葉.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='中通り.紅葉.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='中通り.紅葉.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='中通り.紅葉.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
    )
    ##「中通り.夜空」と受け取った時の処理
    elif content in ['中通り.夜空']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='中通り.夜空.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='中通り.夜空.傷'   
                    ),      
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='中通り.夜空.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='中通り.夜空.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='中通り.夜空.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='中通り.夜空.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,  
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
        ##「中通り.川 or 海」と受け取った時の処理
    elif content in ['中通り.川 or 海']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='中通り.川 or 海.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='中通り.川 or 海.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='中通り.川 or 海.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='中通り.川 or 海.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='中通り.川 or 海.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='中通り.川 or 海.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,  
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
        ##「中通り.森」と受け取った時の処理
    elif content in ['中通り.森']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='中通り.森.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='中通り.森.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='中通り.森.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='中通り.森.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='中通り.森.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='中通り.森.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,  
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
        
        ##「中通り.景色なし」と受け取った時の処理
    elif content in ['中通り.景色なし']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='中通り.景色なし.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='中通り.景色なし.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='中通り.景色なし.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='効能で検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='中通り.景色なし.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='中通り.景色なし.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='なか通り.景色なし.効能なし'
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,  
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )




#「場所無し」分岐
#「場所無し」と受け取った場合の処理
    elif content in ['場所なし']:
        carousel_columns = [
            CarouselColumn(
                text='希望する景色を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='雪景色',
                        data='callback',
                        text='場所なし.雪景色'   
                    ),
                    PostbackTemplateAction(
                        label='紅葉',
                        data='callback',
                        text='場所なし.紅葉'   
                    ),
                
                    PostbackTemplateAction(
                        label='夜空',
                        data='callback',
                        text='場所なし.夜空'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する景色を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='川 or 海',
                        data='callback',
                        text='場所なし.川 or 海'
                    ),
                    PostbackTemplateAction(
                        label='森',
                        data='callback',
                        text='場所なし.森'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='場所なし.効能なし'
                    )
                ]
            )     
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
#「場所無し.雪景色」と受け取った場合の処理
    elif content in ['場所なし.雪景色']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='場所なし.雪景色.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='場所なし.雪景色.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='場所なし.雪景色.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='場所なし.雪景色.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='場所なし.雪景色.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='場所なし.雪景色.効能なし'
                    )
                ]
            )     
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )

    #「場所無し.紅葉」と受け取った場合の処理
    elif content in ['場所なし.紅葉']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='場所なし.紅葉.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='場所なし.紅葉.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='場所なし.紅葉.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='場所なし.川 or 海.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='場所なし.森.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='場所なし.景色なし.効能なし'
                    )
                ]
            )     
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )

    #「場所無し.夜空」と受け取った場合の処理
    elif content in ['場所なし.夜空']:
        carousel_columns = [
            CarouselColumn(
                text='希望する景色を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='場所なし.夜空.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='場所なし.夜空.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='場所なし.夜空.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='場所なし.夜空.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='場所なし.夜空.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='場所なし.夜空.効能なし'
                    )
                ]
            )     
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )

    #「場所無し.川 or 海」と受け取った場合の処理
    elif content in ['場所なし.川 or 海']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='場所なし.川 or 海.美肌'   
                    ),

                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='場所なし.川 or 海.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='場所なし.川 or 海.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する景色を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='場所なし.川 or 海.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='場所なし.川 or 海.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='場所なし.川 or 海.効能なし'
                    )
                ]
            )     
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )
    
    #「場所無し.森」と受け取った場合の処理
    elif content in ['場所なし.森']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='場所なし.森.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='場所なし.森.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='場所なし.森.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='場所なし.森.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='場所なし.森.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='場所なし.森.効能なし'
                    )
                ]
            )     
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )

     #「場所無し.景色なし」と受け取った場合の処理
    elif content in ['場所なし.景色なし']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='場所なし.景色なし.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='場所なし.景色なし.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='場所なし.景色なし.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する効能を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='場所なし.景色なし.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='場所なし.景色なし.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='.希望なし',
                        data='callback',
                        text='場所なし.景色なし.効能なし'
                    )
                ]
            )     
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )


     #「場所なし」と受け取った場合の処理
    elif content in ['場所なし.景色なし.美肌']:
        carousel_columns = [
            CarouselColumn(
                text='希望する効能を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='美肌',
                        data='callback',
                        text='場所なし.景色なし.美肌'   
                    ),
                    PostbackTemplateAction(
                        label='傷',
                        data='callback',
                        text='場所なし.景色なし.傷'   
                    ),
                    PostbackTemplateAction(
                        label='貧血',
                        data='callback',
                        text='場所なし.景色なし.貧血'   
                    )
                ]
            ),
            CarouselColumn(
                text='希望する景色を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='生活習慣病',
                        data='callback',
                        text='場所なし.景色なし.生活習慣病'
                    ),
                    PostbackTemplateAction(
                        label='皮膚病',
                        data='callback',
                        text='場所なし.景色なし.皮膚病'
                    ),
                    PostbackTemplateAction(
                        label='希望なし',
                        data='callback',
                        text='場所なし.景色なし.効能なし'
                    )
                ]
            )     
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )

     #「場所無し.雪景色.美肌」と受け取った場合の処理
    elif content in ['場所なし.雪景色.美肌']:
        carousel_columns = [
            CarouselColumn(
                text='希望する景色を選択してください',
                title='タップで検索',
                actions=[
                    PostbackTemplateAction(
                        label='温泉',
                        data='callback',
                        text='温泉'   
                    )
                ]
            )
        ]
        message_template = CarouselTemplate(columns=carousel_columns)
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='carousel template', template=message_template)
        )

#------------------------------------------------------------------------------------------------------------------------------------------------
#温泉の情報を渡す処理
#------------------------------------------------------------------------------------------------------------------------------------------------
    elif content in ['会津.雪景色.美肌']:
        connection = psycopg2.connect(host='onsen-db-wiz-2.postgres.database.azure.com',
                              user='workuser',
                              password='Postgre0609',
                              database='postgres')
 
        cur = connection.cursor()
        cur.execute('SELECT  onsen_name FROM onsen_table LIMIT 1;')
        results = cur.fetchall()

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text='flex template',contents=results)
        )

    # 「最初から」がタップされた場合の処理
    elif content in ['最初から']:
        response = "改めて窓口を探す際には、もう一度「カテゴリ選択」をタップしてください。"
    # その他              
    else:
        response = "ごめんなさい。メッセージを処理できませんでした。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)) 

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)