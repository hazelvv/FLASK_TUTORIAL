from flask import Flask, request, redirect


app = Flask(__name__)

nextId = 4
topics = [
        {'id': 1, 'title': 'html', 'body': 'html is...'},
        {'id': 2, 'title': 'css', 'body': 'cssl is...'},
        {'id':3, 'title': 'javascript', 'body': 'javascript is...'}

]

def template(contents, content, id=None):
    
    contextUI = ''

    #id가 None이 아니라면 / contextUI 값 생성 - 상세보기로 들어가면 update가 생성됨
    #삭제버튼 추가#
    if id != None:
        contextUI = f'''
            <li><a href ="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type ="submit" value="delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                 {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''



def getContents():
    liTags=''
    #for문으로 리스트 순회#
    for topic in topics:
        #링크생성 <a href>/ id번호생성/ memory에 로드되어있는것 사용/ 현재는 나중에는 DB의 데이터를 읽어오는 코드로 바꿔야함[topics]
        liTags =liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags





@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome</h2>Hello, WEB')
   




@app.route('/read/<int:id>/')
def read(id):
    print(type(id))
    title = ''
    body =''
    for topic in topics:
        if id == topic['id'] : 
            title = topic['title']
            body = topic['body']
            break
    return template(getContents(), f'<h2>{title}</h2>{body}', id)






@app.route('/create/', methods=['GET', 'POST'])
def create():
    print('request.mothod', request.method)
    if(request.method =='GET'):
        content = '''
            
            <form action="/create/" method="POST">
                <p><input type ="text" name="title" placeholder="title"></p>
                <p><textarea name="body"placeholder ="body"> </textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method =='POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        newTopic ={'id': nextId, 'title': title, 'body':body}
        topics.append(newTopic)
        url =  '/read/'+str(nextId)+'/'
        nextId = nextId + 1
        return redirect(url)
    

#업데이트
@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    print('request.mothod', request.method)
    if(request.method =='GET'):
        title = ''
        body =''
        for topic in topics:
            if id == topic['id'] : 
                title = topic['title']
                body = topic['body']
                break
       

        content = f'''
            
            <form action="/update/{id}/" method="POST">
                <p><input type ="text" name="title" placeholder="title" value="{title}"></p>
                <p><textarea name="body"placeholder ="body"> {body} </textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method =='POST':
        global nextId
        title = request.form['title']
        body = request.form['body']

        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break

        url =  '/read/'+str(id)+'/'
        return redirect(url)
    


@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')    
    

if __name__ == '__main__':
    app.run(debug=True)
