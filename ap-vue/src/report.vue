<template>
    <div id="app">
        <el-menu
                :default-active="activeIndex"
                class="el-menu-demo"
                mode="horizontal"
                @select="handleSelect"
                background-color="#545c64"
                text-color="#fff"
                active-text-color="#ffd04b">
            <el-menu-item index="1"><v-link href="/"><div style="width: 100%">接口测试</div></v-link></el-menu-item>
            <el-menu-item index="2"><v-link href="/spiderBatch"><div style="width: 100%">批量执行</div></v-link></el-menu-item>
            <el-menu-item index="3"><v-link href="/scheduler"><div style="width: 100%">定时任务</div></v-link></el-menu-item>
            <el-menu-item index="4"><v-link href="/report"><div style="width: 100%">执行报告</div></v-link></el-menu-item>
            <el-menu-item index="5"><v-link href="/search"><div style="width: 100%">记录查询</div></v-link></el-menu-item>
            <el-menu-item index="6" disabled>消息中心</el-menu-item>
        </el-menu>
            <div style="position: absolute;left: 5%;top: 15%;">

            <el-select v-model="taskID" placeholder="请选择任务" @change="getReport">
                <el-option
                        v-for="item in options"
                        :key="item.id"
                        :label="item.name"
                        :value="item.id"
                        selected="0">
                </el-option>
            </el-select>
            </div>
            <div style="margin-top: 15px"></div>
            <div class="myChart" :style="{width: '300px', height: '300px',margin:'auto'}"></div>
            <div class="myChart" :style="{width: '1400px', height: '300px',margin:'auto'}"></div>

            <div id="robot" @click="robotWeiXingDialog = true">
                <img src="./assets/auto.png"/>
            </div>

            <el-dialog
                title="自动化测试助手"
                :visible.sync="robotWeiXingDialog"
                width="42%"
                center>
                <div id="robotbig"><img src="./assets/auto_big.jpg" /></div>
                <span slot="footer" class="dialog-footer">
                    自动化测试工具小程序。PC端自动化测试平台的辅助工具。可一键执行批量测试，也可方便的查看用例详情，执行结果和执行报告。
                </span>
            </el-dialog>

            <div id="footer" class="flex-hor-center">
                <span>© 2018-2019 automation created by 郭家兴 | 晋ICP备18013433号</span>
            </div>

        </div>
</template>
<script>
import VLink from './VLink.vue'
    export default {
	components: {
      VLink
    },
        data() {
            return {
                robotWeiXingDialog: false,
                activeIndex: '4',
                reportDate:{},
                c:{},
                cicleData:[
                    {value:null, name:'未执行'},
                    {value:null, name:'成功'},
                    {value:null, name:'失败'}
                ],
                lineDate:{
                    pass_probability:[],
                    fail_probability:[],
                    execute_probability:[]
                },
                options:[],
                taskID:0
            }
        },
        watch:{
            cicleData:{

                handler:function(val,oldval){

                    this.pie();

                },

                deep:true//对象内部的属性监听，也叫深度监听

            },
            lineDate:{

                handler:function(val,oldval){

                    this.linechart();

                },

                deep:true//对象内部的属性监听，也叫深度监听

            },

        },
        mounted:function (){
            this.getTask();
            this.pie();
            this.linechart();

        },
        methods: {
            /*获取任务列表*/
            getTask:function() {
                const _self = this;
                $.ajax({
                    type: "GET",
                    url: window.URL + "/v1/task/allTask",
                    contentType: "application/json",
                    data: JSON.stringify(this.sendParams),
                    success: function (r) {
                        _self.options = r;
                        _self.taskID = r[0].id
                        _self.getReport(r[0].id);
                    },
                    error: function (r) {

                    }
                });
            },
            getReport:function(task_id){
                this.taskID = task_id
                const _self = this;
                $.ajax({
                    type: "GET",
                    url: window.URL + "/v1/task/getReportDate?task_id=" + this.taskID,
                    contentType: "application/json",
                    data: JSON.stringify(this.sendParams),
                    success: function (r) {
                        var pass_num = 0;
                        var fail_num = 0;
                        var execute_num = 0;
                        var total = 0;
                        for(var key in r) {
                            if(r[key]['cicle']==true){
                                pass_num = r[key]['pass_num'];
                                fail_num = r[key]['fail_num'];
                                total = r[key]['total'];
                                execute_num = r[key]['execute_num'];

                            }
                        }
                        var not_excete_num=total-execute_num;
                        _self.cicleData = [
                            {value:not_excete_num, name:'未执行'},
                            {value:pass_num, name:'成功'},
                            {value:fail_num, name:'失败'}
                        ];
                        _self.lineDate.pass_probability = [];
                        _self.lineDate.fail_probability = [];
                        _self.lineDate.execute_probability = [];
                        for(var key in r){
                            _self.lineDate.pass_probability.push(r[key]['pass_probability']);
                            _self.lineDate.fail_probability.push(r[key]['fail_probability']);
                            _self.lineDate.execute_probability.push(r[key]['execute_probability']);
                        }
                        console.log(_self.lineDate);
                        _self.reportDate = r;
                    },
                    error: function (r) {
                        if (r.responseJSON.error_code) {
                            loading.close();
                            _self.openError("暂无报表数据");
                        }
                    }
                });
            },
            pie(){
                // 基于准备好的dom，初始化echarts实例
                let myChart = this.$echarts.init(document.getElementsByClassName('myChart')[0])
                // 绘制图表
                myChart.setOption({
                    title : {
                        text: '',
                        subtext: '最新记录',
                        x:'center'
                    },
                    color:['#E6A23C', '#67C23A','#F56C6C'],
                    tooltip : {
                        trigger: 'item'
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left',
                        data: ['未执行','成功','失败']
                    },
                    series : [
                        {
                            name: '执行情况',
                            type: 'pie',
                            radius : '50%',
                            center: ['50%', '50%'],
                            data:this.cicleData,
                            itemStyle: {
                                emphasis: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                }
                            }
                        }
                    ]
                });
            },
            linechart(){
                // 基于准备好的dom，初始化echarts实例
                let myChart = this.$echarts.init(document.getElementsByClassName('myChart')[1]);
                // 绘制图表
                myChart.setOption({
                    title: {
                        text: '一周执行情况'
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    legend: {
                        data:['通过率','失败率','执行率']
                    },
                    color:[ '#67C23A','#F56C6C','#E6A23C'],
                    grid: {
                        left: '6%',
                        right: '6%',
                        bottom: '3%',
                        containLabel: true
                    },
                    toolbox: {
                        feature: {
                            saveAsImage: {}
                        }
                    },
                    xAxis: {
                        type: 'category',
                        boundaryGap: false,
                        data: ['周一','周二','周三','周四','周五','周六','周日']
                    },
                    yAxis: [
                        {
                        type: 'value',
                        axisLabel:{
                            formatter:'{value} %'
                        },
                        max: 100,
                        min: 0,

                    },
                        {
                            type: 'value',
                            axisLabel:{
                                formatter:'{value} %'
                            },
                            show : false,
                             max: 100,
                             min: 0,

                        },
                        {
                            type: 'value',
                            axisLabel:{
                                formatter:'{value} %'
                            },
                            show : false,
                             max: 100,
                             min: 0,

                        }
                    ],
                    series: [
                        {
                            name:'通过率',
                            type:'line',
                            data:this.lineDate.pass_probability,
                            yAxisIndex:0
                        },
                        {
                            name:'失败率',
                            type:'line',
                            data:this.lineDate.fail_probability,
                            yAxisIndex:1
                        },
                        {
                            name:'执行率',
                            type:'line',
                            data:this.lineDate.execute_probability,
                            yAxisIndex:2
                        }
                    ]
                });
                var m = this.reportDate;
                myChart.on('click', function (params) {
                    var l = [];
                    var d = '';
                    for(var key in m){
                        l.push(key);
                    }
                    d =l[params.dataIndex];

                    console.log(params);
                });

            },

            openFullScreen() {
                const loading = this.$loading({
                    lock: true,
                    text: 'Loading',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                });
                setTimeout(() => {
                    loading.close();
                }, 5000);
            }
        }
    }
</script>

<style scoped>
    #app {
        font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
        text-align: center;
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
    }
    #table{
        display: inline-block;
        margin-top:25px ;

    }
    .el-scrollbar__wrap {
        overflow-x: hidden;
    }

    .el-row {
        padding-top: 15px;
        margin-left: 0 ! important ;
        margin-right: 0 ! important ;
    }

    .grid-content2 {
        border-radius: 6px;
        min-height: 6px;
        background: #409EFF;

    }

    .grid-content {
        border-radius: 4px;
        min-height: 3px;
        background: #99a9bf;

    }

    .el-radio-group {
        width: 66.5%;
    }

    #footer {
        color: #9a9b9c;
        font-weight: 400;
        position: absolute;
        bottom: 4%;
        width: 97%;
    }
    .flex-hor-center {
        display: flex;
        justify-content: center;
    }
    .elbtn{
        margin: 0;
    }
    [v-cloak] {
        display: none
    }
    .el-col {
        height: 40px;
    ;
    }

    .active{
        background: rgba(1, 144, 254, 0.51);
         color: #fff;
    }
    .select{
        background: rgb(1, 144, 254);
        color: #fff;
    }
    .el-table th {
        -moz-user-select: none;
        text-align: center !important;
    }
    .el-table__column-filter-trigger i {
        color: #f2f6fc;
    }
    .el-table th>.cell.highlight {
        color: #ffbd40;
    }
    .el-table__column-filter-trigger {
        display: inline-block;
        line-height: 23px;
        cursor: pointer;
    }
    .closebtn {
        position: absolute;
        top: 10px;
        right: 10px;
        padding: 0;
        background: 0 0;
        border: none;
        outline: 0;
        cursor: pointer;
        font-size: 16px;
    }

    #robot {
        position: absolute;
        top: 20%;
        right: 5px;
    }
    #robot img{
        height: 50px;
        width: 50px;
        cursor:pointer;
    }
    #robotbig{
        text-align: center;
    }

</style>
