<template>
    <div id="app">
        <el-container>
            <el-header>
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
        </el-header>
            <el-main>
            <el-container>
                <el-container>
                    <el-aside width="350px">
                        <el-form ref="searchForm" :model="form" label-width="90px">
                        <el-row style="margin-top: 22px">
                            <el-col :span="18" :offset="3" >
                                <el-form-item label="定时名称:">
                                    <el-input v-model="form.scheduler_id" placeholder="" disabled></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="18" :offset="3" >
                                    <el-form-item label="任务名称:">
                                    <el-select v-model="form.taskID" placeholder="请选择任务">
                                        <el-option
                                                :disabled="add_or_edit==0"
                                                v-for="item in options"
                                                :key="item.id"
                                                :label="item.name"
                                                :value="item.id"
                                                >
                                        </el-option>
                                    </el-select>
                                    </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="18" :offset="3" >
                                    <el-form-item label="执行周期:">
                                        <el-input v-model="form.day_of_week" placeholder="mon-sun"></el-input>
                                    </el-form-item>
                            </el-col>
                        </el-row>
                            <el-row>
                                <el-col :span="18" :offset="3" >
                                    <el-form-item label="执行时间:">
                                        <el-time-picker
                                                v-model="form.time"
                                                style="width: auto"
                                                format="HH:mm"
                                                :picker-options="{

                                                        }"
                                                placeholder="05:30">
                                        </el-time-picker>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="18" :offset="3" >
                                    <el-form-item label="维护人员:">
                                        <el-select v-model="form.user_id" placeholder="">
                                            <el-option
                                                    v-for="item in user_options"
                                                    :key="item.id"
                                                    :label="item.nickname"
                                                    :value="item.id"
                                            >
                                            </el-option>
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-col :span="18" :offset="3" >
                                    <el-form-item label="抄送人邮箱:">
                                        <el-input v-model="form.copy_person" placeholder="请填写抄送人邮箱账号"></el-input>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                            <el-row>
                                <el-button v-if="add_or_edit==1" type="primary" icon="el-icon-circle-plus-outline" @click="addJob">新增</el-button>
                                <el-button v-if="add_or_edit==0" type="primary" icon="el-icon-edit" style="margin-left: 10px" @click="updateJob">编辑</el-button>
                                <el-button v-if="add_or_edit==0"   @click="exitEdit" style="margin-left: 20px">取消</el-button>
                            </el-row>
                        </el-form>
                    </el-aside>

                        <el-main>
                            <el-table
                                    :data="tableData"
                                    stripe
                                    height="585px"
                                    style="width: 100%">
                                <el-table-column
                                        label=""
                                        width="45"
                                        fixed>
                                    <template slot-scope="scope">
                                        <el-button v-if="scope.row.running_state==0"  type="danger"  size="mini" circle></el-button>
                                        <el-button v-else-if="scope.row.running_state==1"  type="success"  size="mini" circle></el-button>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="定时任务编号"
                                        width="180"
                                        :show-overflow-tooltip="true"
                                        fixed>
                                    <template slot-scope="scope">
                                        <span style="margin-left: 5px">{{ scope.row.scheduler_id }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="任务"
                                        :show-overflow-tooltip="true"
                                        width="180">
                                    <template slot-scope="scope">
                                        <span style="margin-left: 5px">{{ scope.row.task.name }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="下次执行时间"
                                        :show-overflow-tooltip="true"
                                        width="160">
                                    <template slot-scope="scope">
                                        <span style="margin-left: 5px">{{ scope.row.next_run_time }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="执行周期"
                                        :show-overflow-tooltip="true"
                                        width="150">
                                    <template slot-scope="scope">
                                        <span style="margin-left: 5px">{{ scope.row.day_of_week }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="执行时间"
                                        :show-overflow-tooltip="true"
                                        width="130">
                                    <template slot-scope="scope">
                                        <i class="el-icon-time"></i>
                                        <span style="margin-left: 5px">{{ scope.row.hour+":"+scope.row.minute}}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="维护人"
                                        :show-overflow-tooltip="true"
                                        width="180">
                                    <template slot-scope="scope">
                                        <span style="margin-left: 5px">{{ scope.row.user.nickname }}</span>
                                    </template>
                                </el-table-column>
                                <el-table-column
                                        label="抄送人"
                                        :show-overflow-tooltip="true"
                                        align="left"
                                        width="280">
                                    <template slot-scope="scope">
                                        <i v-if="scope.row.copy_person" class="el-icon-message"></i>
                                        <span style="margin-left: 5px">{{ scope.row.copy_person }}</span>
                                    </template>
                                </el-table-column>

                                <el-table-column label="操作"
                                                 fixed="right"
                                width="265">
                                    <template slot-scope="scope">
                                        <el-button
                                                size="mini"
                                                type="success"
                                                :disabled="scope.row.running_state==1"
                                                @click="startJob(scope.$index, scope.row)">启动</el-button>
                                        <el-button
                                                size="mini"
                                                type="warning"
                                                :disabled="scope.row.running_state==0"
                                                @click="pauseJob(scope.$index, scope.row)">停止</el-button>
                                        <el-button
                                                size="mini"
                                                type="primary"
                                                @click="edit(scope.$index, scope.row)">编辑</el-button>
                                        <el-button
                                                size="mini"
                                                type="danger"
                                                @click="deleteJob(scope.$index, scope.row)">删除</el-button>
                                    </template>
                                </el-table-column>
                            </el-table>

                        </el-main>

                </el-container>
            </el-container>


            <div id="footer" class="flex-hor-center">
                <span>© 2018-2019 automation created by 郭家兴 | 晋ICP备18013433号</span>
            </div>

        </el-main>
        </el-container>
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
                activeIndex: '3',
                options:[],
                taskMap:{},
                user_options:[],
                add_or_edit:1,
                tableData:[{
                    scheduler_id:234166
                },
                    {
                        scheduler_id:234166
                    }],
                form:{
                    scheduler_id:'',
                    taskID:0,
                    day_of_week:'',
                    time:new Date(2016, 9, 10, 5, 30),
                    user_id:2,
                    copy_person:'',

                }
            }
        },
        watch:{

        },
        mounted:function (){
            this.getTask();
            this.getUsers();
            this.getAllJobs();

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
                        _self.form.taskID = r[0].id
                    },
                    error: function (r) {

                    }
                });
            },
            exitEdit:function(){
                this.add_or_edit=1;
                this.form = {
                    scheduler_id:'',
                    taskID:this.options[0].id,
                    day_of_week:'',
                    time:new Date(2016, 9, 10, 5, 30),
                    user_id:this.user_options[2].id,
                    copy_person:'',
                }

            },
            getAllJobs:function () {
                const loading = this.$loading({
                    lock: true,
                    text: 'Loading',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)',
                    target: document.querySelector('#app')
                });
                const _self = this;
                $.ajax({
                    type: "GET",
                    url: window.URL + "/v1/task/getJobs",
                    contentType: "application/json",
                    data: JSON.stringify(this.sendParams),
                    success: function (r) {
                        _self.tableData = r;
                        loading.close();

                    },
                    error: function (r) {
                        loading.close();
                    }
                });
            },
            getUsers:function(){
                const _self = this;
                $.ajax({
                    type: "GET",
                    url: window.URL + "/v1/user/getUser/0",
                    contentType: "application/json",
                    data: JSON.stringify(this.sendParams),
                    success: function (r) {
                        _self.user_options = r;
                        _self.form.user_id = r[2].id
                    },
                    error: function (r) {

                    }
                });
            },
            deleteJob:function(index,row){
                this.$confirm('此操作将永久删除该定时任务, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    const _self = this;
                    $.ajax({
                        type: "GET",
                        url: window.URL + "/v1/task/deleteJob?scheduler_id="+row.scheduler_id,
                        contentType: "application/json",
                        data: JSON.stringify(this.sendParams),
                        success: function (r) {
                            _self.getAllJobs();
                            _self.$message({
                                message: '删除定时任务成功',
                                type: 'success'
                            });

                        },
                        error: function (r) {
                            _self.$message.error('删除定时任务失败');

                        }
                    });
                }).catch(() => {

                });
            },
            startJob:function(index,row){
                const _self = this;
                $.ajax({
                    type: "GET",
                    url: window.URL + "/v1/task/startJob?scheduler_id="+row.scheduler_id,
                    contentType: "application/json",
                    data: JSON.stringify(this.sendParams),
                    success: function (r) {
                        _self.getAllJobs();
                        _self.$message({
                            message: '启动定时任务成功',
                            type: 'success'
                        });

                    },
                    error: function (r) {
                        _self.$message.error('启动定时任务失败');

                    }
                });
            },
            pauseJob:function(index,row){
                const _self = this;
                $.ajax({
                    type: "GET",
                    url: window.URL + "/v1/task/pauseJob?scheduler_id="+row.scheduler_id,
                    contentType: "application/json",
                    data: JSON.stringify(this.sendParams),
                    success: function (r) {
                        _self.getAllJobs();
                        _self.$message({
                            message: '停止定时任务成功',
                            type: 'success'
                        });

                    },
                    error: function (r) {
                        _self.$message.error('停止定时任务失败');
                    }
                });
            },
            updateJob:function(){
                const loading = this.$loading({
                    lock: true,
                    text: 'Loading',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)',
                    target: document.querySelector('#app')
                });
                const _self = this;
                if (_self.form.day_of_week==''){
                    _self.form.day_of_week='mon-sun';
                }
                this.sendParams = {
                    scheduler_id :this.form.scheduler_id,
                    day_of_week :this.form.day_of_week,
                    hour :this.form.time.getHours(),
                    minute :this.form.time.getMinutes(),
                    user_id :this.form.user_id,
                    copy_person :this.form.copy_person,
                };
                $.ajax({
                    type: "POST",
                    url: window.URL + "/v1/task/updateJob",
                    contentType: "application/json",
                    data: JSON.stringify(this.sendParams),
                    success: function (r) {
                        _self.getAllJobs();
                        _self.exitEdit();
                        _self.$alert('编辑成功！', '提示', {
                            confirmButtonText: '确定',
                            callback: action => {
                                this.$message({
                                    type: 'info',
                                    message: `action: ${ action }`
                                });
                            }
                        });
                        _self.form = {
                            scheduler_id :'',
                            day_of_week :'',
                            time:new Date(2016, 9, 10, 5, 30),
                            copy_person :'',
                            user_id: _self.user_options[2].id,
                            taskID: _self.options[0].id
                        };
                        loading.close();
                    },
                    error: function (r) {
                        if (r.responseJSON.error_code) {
                            loading.close();
                            _self.openError("编辑失败");
                        }
                    }
                });

            },
            addJob:function(){
                const loading = this.$loading({
                    lock: true,
                    text: 'Loading',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)',
                    target: document.querySelector('#app')
                });
                const _self = this;
                if (_self.form.day_of_week==''){
                    _self.form.day_of_week='mon-sun';
                }
                this.sendParams = {
                    task_id :this.form.taskID,
                    day_of_week :this.form.day_of_week,
                    hour :this.form.time.getHours(),
                    minute :this.form.time.getMinutes(),
                    user_id :this.form.user_id,
                    copy_person :this.form.copy_person,
                };
                $.ajax({
                    type: "POST",
                    url: window.URL + "/v1/task/addJob",
                    contentType: "application/json",
                    data: JSON.stringify(this.sendParams),
                    success: function (r) {
                        _self.getAllJobs();
                        _self.form.day_of_week='';
                        _self.$alert('新增成功！', '提示', {
                            confirmButtonText: '确定',
                            callback: action => {
                                this.$message({
                                    type: 'info',
                                    message: `action: ${ action }`
                                });
                            }
                        });
                        _self.form = {
                            scheduler_id :'',
                            day_of_week :'',
                            time:new Date(2016, 9, 10, 5, 30),
                            copy_person :'',
                            user_id: _self.user_options[2].id,
                            taskID: _self.options[0].id
                        };
                        loading.close();
                    },
                    error: function (r) {
                        if (r.responseJSON.error_code) {
                            loading.close();
                            _self.openError("新增失败");
                        }
                    }
                });

            },
            edit:function(index,row){
                this.add_or_edit=0;
                this.form.taskID = row.task.id;
                this.form.scheduler_id = row.scheduler_id;
                this.form.day_of_week = row.day_of_week;
                this.form.time = new Date(2016, 9, 10, row.hour, row.minute);
                this.form.user_id = row.user.id;
                this.form.copy_person = row.copy_person;
            },
            openError(msg) {
                this.$message.error(msg);
            },
            openWarn(msg) {
                this.$message({
                    message: msg,
                    type: 'warning'
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
    function scrollbarShowHidden(element){
        element.addClass('scrollbarHide');
        element.hover(function() {
            element.addClass('scrollbarShow');
        }, function() {
            element.removeClass('scrollbarShow');
        });

    }

    scrollbarShowHidden($('el-table__body-wrapper'));
</script>

<style >
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
    .el-button+.el-button {
        margin-left: 0;
    }
        .el-header {
    padding: 0;
    }

    .el-main {
    padding: 10px;
    }

    .el-container {
    height: 100%;
    }
    .el-aside{
        font-weight: 600;
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

    *::-webkit-scrollbar {width:7px; height:10px; background-color:transparent;} /*定义滚动条高宽及背景 高宽分别对应横竖滚动条的尺寸*/
    *::-webkit-scrollbar-track {background-color:#f0f6ff;  } /*定义滚动条轨道 内阴影+圆角*/
    *::-webkit-scrollbar-thumb {background-color: rgba(96, 96, 96, 0.2); border-radius:6px;} /*定义滑块 内阴影+圆角*/
    .scrollbarHide::-webkit-scrollbar{display: none}
    .scrollbarShow::-webkit-scrollbar{display: block}


</style>
