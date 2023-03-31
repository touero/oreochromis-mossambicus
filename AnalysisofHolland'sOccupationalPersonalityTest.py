from pywebio.input import *
from pywebio.output import *
from pyecharts import options as opts
from pyecharts.charts import Radar
from pyecharts.globals import ThemeType
import pandas as pd
import pywebio


def base():
    pywebio.config(title='霍兰德职业性格测试平台')  # 标题
    # ui设计
    put_markdown('#')
    put_markdown('# 霍兰德职业性格测试分析')
    put_markdown("## Analysis of Holland's Occupational Personality Test")
    toast("请完成下面各题共90题，符合请选择Yes否则为No", 5, 'center', 'success')  # 通知消息
    order = []
    question = []
    choice = []
    types = []
    with open('testQuestions.txt', 'r', encoding='utf-8') as file:
        for lines in file:
            line = lines.replace('\n', '')
            ord = line.split('．')[0]
            order.append(ord)
            if int(ord) % 6 == 1:
                types.append('现实型')
            if int(ord) % 6 == 2:
                types.append('研究型')
            if int(ord) % 6 == 3:
                types.append('艺术型')
            if int(ord) % 6 == 4:
                types.append('社会型')
            if int(ord) % 6 == 5:
                types.append('企业型')
            if int(ord) % 6 == 0:
                types.append('常规型')
            sel = select('{}'.format(line), ["Yes", "No"])
            choice.append(sel)
            que = line.split('．')[1]
            question.append(que)

    data = pd.DataFrame({'order': order, 'question': question, 'types': types, 'choice': choice})
    dfYes = data[data.choice == 'Yes']
    countYes = dfYes['types'].value_counts(ascending=False)
    maxType = countYes[0:3].index.tolist()
    countYesList = [countYes.tolist()]
    result = []
    with open('result.txt', 'r', encoding='utf-8') as file:
        for lines in file:
            result.append(lines)
    return countYes, countYesList, maxType, result


def drawing(countYes, countYesList, maxType, result):
    radar = Radar({"theme": ThemeType.DARK})
    radar.add_schema(
        schema=[
            opts.RadarIndicatorItem(name='{}'.format(countYes.index.tolist()[0]), max_=15),
            opts.RadarIndicatorItem(name='{}'.format(countYes.index.tolist()[1]), max_=15),
            opts.RadarIndicatorItem(name='{}'.format(countYes.index.tolist()[2]), max_=15),
            opts.RadarIndicatorItem(name='{}'.format(countYes.index.tolist()[3]), max_=15),
            opts.RadarIndicatorItem(name='{}'.format(countYes.index.tolist()[4]), max_=15),
            opts.RadarIndicatorItem(name='{}'.format(countYes.index.tolist()[5]), max_=15),
        ]
    )
    radar.add('题目类型选择统计', countYesList, color='red',
              areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='pink'))
    radar.set_global_opts(title_opts=opts.TitleOpts(title='霍兰德职业性格测试结果'),
                          legend_opts=opts.LegendOpts(selected_mode='single'))  # 通过legend设置单例模式
    toast("测试成功", 5, 'center', 'success')
    put_markdown(
        '测评结果中，最高分数的类型即第一位是主要类型，排在后两位类型可按照上表进行一定的推断与验证。如第一位是艺术型，第二位是社会型或研究型的职业兴趣也是可以考虑用来求职的，若是常规型则说明兴趣类型方面有一定的冲突，需要其他的测评或指导。')
    put_markdown("## 您职业兴趣测试定性依次为：")
    for maxtype in maxType:
        put_markdown("## " + maxtype)
        if maxtype == '艺术型':
            put_markdown(result[0])
            put_markdown(result[1])
        if maxtype == '常规型':
            put_markdown(result[2])
            put_markdown(result[3])
        if maxtype == '企业型':
            put_markdown(result[4])
            put_markdown(result[5])
        if maxtype == '研究型':
            put_markdown(result[6])
            put_markdown(result[7])
        if maxtype == '现实型':
            put_markdown(result[8])
            put_markdown(result[9])
        if maxtype == '社会型':
            put_markdown(result[10])
            put_markdown(result[11])
    return radar.render_notebook()


if __name__ == '__main__':
    countYes, countYesList, maxType, result = base()
    put_html(drawing(countYes, countYesList, maxType, result))
