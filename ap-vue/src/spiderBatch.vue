<template>
    <div id="app">
        <el-container>
            <el-header>
                <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
                    <el-menu-item index="1">
                        <v-link href="/">
                            <div style="width: 100%">接口测试</div>
                        </v-link>
                    </el-menu-item>
                    <el-menu-item index="2">
                        <v-link href="/spiderBatch">
                            <div style="width: 100%">批量执行</div>
                        </v-link>
                    </el-menu-item>
                    <el-menu-item index="3">
                        <v-link href="/scheduler">
                            <div style="width: 100%">定时任务</div>
                        </v-link>
                    </el-menu-item>
                    <el-menu-item index="4">
                        <v-link href="/report">
                            <div style="width: 100%">执行报告</div>
                        </v-link>
                    </el-menu-item>
                    <el-menu-item index="5">
                        <v-link href="/search">
                            <div style="width: 100%">记录查询</div>
                        </v-link>
                    </el-menu-item>
                    <el-menu-item index="6" disabled>消息中心</el-menu-item>
                </el-menu>
            </el-header>
            <el-main>

                <el-form ref="searchForm" :model="searchForm" label-width="80px">
                    <el-row :gutter="10">
                      <el-col :span="1" :offset="1">
                        <div @click="rotationButton" id="rotation" @mouseover="rotationButton" @mouseout="rotationButton">
                        <el-button type="primary" size="mini" icon="el-icon-caret-top" circle @click="leftBox=!leftBox"></el-button>
                      </div>
                      </el-col>
                        <el-col :span="4" :offset="3">
                            <el-form-item label="用例名称:" style="font-weight:600">
                                <el-input v-model="searchForm.name" size="large" placeholder="请输入用例名称"></el-input>
                            </el-form-item>

                        </el-col>
                        <el-col :span="7">
                            <el-form-item label="URL:" style="font-weight:600">
                                <el-input v-model="searchForm.url" size="large" placeholder="请输入url"></el-input>
                            </el-form-item>

                        </el-col>
                        <el-col :span="2">
                            <el-button type="primary" size="medium" @click="handleCurrentChange(1)" icon="el-icon-search" :disabled="selectTaskId==''"> 搜索</el-button>
                        </el-col>
                        <el-button type="primary" size="medium" @click="openFormBox" :disabled="selectTaskId==''"> 新增</el-button>
                        <el-button type="primary" size="medium" @click="send" :disabled="selectTaskId==''"> 运行</el-button>
                        <el-button type="primary" size="medium" icon="el-icon-upload" @click="upLoad"> 导入</el-button>

                    </el-row>
                </el-form>

                <el-row>
                    <el-col style="height: 3px">
                        <div class="grid-content"></div>
                    </el-col>
                </el-row>
                <div style="text-align: center">
                    <div id="table">
                        <el-table @row-click="showCaseDetail" :header-cell-style="{background:'#409EFF',color:'#FFFFFF',align:'center'}" :row-style="rowStyle" v-loading="loading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(143, 188, 143, 0.8)" :data="tableData" height="485" stripe highlight-current-row="true" border style="width: 100%">
                            <el-table-column type="index" label="序号" width="80" align="center">
                            </el-table-column>
                            <el-table-column prop="case_id" label="用例编号" width="130" :show-overflow-tooltip="true" align="center">
                            </el-table-column>
                            <el-table-column prop="case_name" label="用例名称" width="180" :show-overflow-tooltip="true" align="left">
                            </el-table-column>
                            <el-table-column prop="url" label="URL" width="320" :show-overflow-tooltip="true" align="left">
                            </el-table-column>
                            <el-table-column prop="method" label="请求方法" width="130" align="center">
                            </el-table-column>
                            <el-table-column prop="dependent_case" label="依赖用例" width="180" :show-overflow-tooltip="true" align="center">
                            </el-table-column>
                            <el-table-column prop="is_run" label="是否执行" width="80" :show-overflow-tooltip="true" align="center">
                                <template slot-scope="scope">
                                    <span v-if="scope.row.is_run">是</span>
                                    <span v-else>否</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="actual_result" label="实际结果" width="130" :filters="[{ text: '失败', value: '0' }, { text: '通过', value: '1' }]" :filter-method="filterTag" filter-placement="bottom-end" align="center">
                                <template slot-scope="scope">
                                    <el-tag v-if="scope.row.actual_result === '0'" type="danger" size="medium " disable-transitions>失败</el-tag>
                                    <el-tag v-if="scope.row.actual_result === '1'" type="success" size="medium " disable-transitions>通过</el-tag>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" align="center" width="150">
                                <template slot-scope="scope">
                                    <el-button size="mini" @click.stop="openFormBoxEdit(scope.$index, scope.row)">编辑
                                    </el-button>
                                    <el-button size="mini" type="danger" @click.stop="deleteTaskCase(scope.$index, scope.row)">删除
                                    </el-button>
                                </template>
                            </el-table-column>

                        </el-table>

                    </div>
                </div>
                <el-row>
                    <el-col :span="4" :offset="16">
                        <div class="block">
                            <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :page-size="8" layout="total,prev, pager, next, jumper" :total="pagination.total" :current-page="pagination.page">
                            </el-pagination>
                        </div>
                    </el-col>
                </el-row>

                <div class='popContainer' v-show="fromBox">

                    <div class="caseForm">
                        <el-scrollbar style="height: 100%;">
                            <div style="margin: 30px;font-size: large"><span v-if="this.form_add_or_edit==0">新增用例</span><span v-else-if="this.form_add_or_edit==1">编辑用例</span></div>
                            <el-form ref="form" :model="form" label-width="80px">
                                <el-row :gutter="10">
                                    <el-col :span="6" :offset="2">
                                        <el-form-item label="用例编号:">
                                            <el-input v-model="form.case_id" size="large" disabled=""></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span="7" :offset="1">
                                        <el-form-item label="用例名称:">
                                            <el-input v-model="form.case_name" size="large" placeholder="请输入用例名称"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span="1" style="padding-top: 0px;" :offset="1">
                                        <el-form-item label="是否执行:">
                                            <el-switch v-model="form.is_run" active-color="#409EFF" inactive-color="#C0CCDA">
                                            </el-switch>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row :gutter="10">
                                    <el-col :span="6" :offset="2">
                                        <el-form-item label="请求方式:" :value="form.method">
                                            <el-select v-model="form.method">
                                                <el-option label="GET" value="get" selected="selected"></el-option>
                                                <el-option label="POST" value="post"></el-option>
                                                <el-option label="PUT" value="put"></el-option>
                                                <el-option label="DELETE" value="delete"></el-option>
                                            </el-select>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span="12" :offset="1">
                                        <el-form-item label="URL:">
                                            <el-input v-model="form.url" size="large" placeholder="请输入url"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row :gutter="10">
                                    <el-col :span="6" :offset="2">
                                        <el-form-item label="后置处理:" :value="form.deal_method">
                                            <el-select v-model="form.deal_method">
                                                <el-option label="不做处理" value="0" selected="selected"></el-option>
                                                <el-option label="默认处理" value="1"></el-option>
                                                <el-option label="获取key值保存" value="2"></el-option>
                                                <el-option label="正则表达式" value="3"></el-option>
                                            </el-select>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span="12" :offset="1">
                                        <el-form-item label="处理条件:">
                                            <el-input v-model="form.need_position" size="large" placeholder="请输入处理条件"></el-input>
                                        </el-form-item>
                                    </el-col>

                                </el-row>
                                <el-row :gutter="10">
                                    <el-col :span="6" :offset="2">
                                        <el-switch style="display: block;margin-top: 8px" v-model="form.submission" active-color="#13ce66" inactive-color="#ff4949" active-text="json提交" inactive-text="form提交">
                                        </el-switch>
                                    </el-col>
                                    <el-col :span="7" :offset="1">
                                        <el-form-item label="依赖用例:">
                                            <el-select v-model="form.dependent_case" multiple filterable placeholder="请选择依赖用例" style="width: 215%;">
                                                <el-option v-for="item in form.options" :key="item.value" :label="item" :value="item">
                                                </el-option>
                                            </el-select>

                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row :gutter="10" style="height: 150px">
                                    <el-col :span="19" :offset="2">
                                        <el-form-item label="header:">
                                            <el-input type="textarea" :rows="5" placeholder="请输入请求参数" v-model="form.header">
                                            </el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row :gutter="10" style="height: 150px">
                                    <el-col :span="19" :offset="2">
                                        <el-form-item label="data:">
                                            <el-input type="textarea" :rows="5" placeholder="请输入请求参数" v-model="form.data">
                                            </el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row :gutter="10" style="height: 150px">
                                    <el-col :span="19" :offset="2">
                                        <el-form-item label="预期结果:">
                                            <el-input type="textarea" :rows="5" placeholder="请输入预期结果" v-model="form.expect_result">
                                            </el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>

                                <el-button type="primary" @click="addEditCase" style="margin: 20px">确定</el-button>

                                <el-button style="margin: 20px" @click="closeFormBox">取消</el-button>

                            </el-form>
                        </el-scrollbar>
                    </div>

                </div>
                <el-collapse-transition>
                    <div class='popContainer2' v-show="leftBox">
                        <el-button type="primary" icon="el-icon-circle-plus-outline" @click="openTaskBox" style="margin: 18px">新增任务</el-button>
                        <div class="grid-content2"></div>
                        <el-scrollbar style="height: 100%;">
                            <div>
                                <ul>
                                    <li v-for="(item,index) in list1" :key="index" @mouseenter="mouseEnter(index)" @mouseleave="mouseLeave" @click="selectTask(index,item.id)" :class="[{'active':index==isActive},{'select':index==isSelect}]">
                                        <div>
                                            <div>
                                                <el-row>
                                                    <el-col :span="12" :offset="2" style="text-align: left">
                                                        <el-tooltip class="item" effect="dark" placement="right-end" v-if=item.description>
                                                            <div slot="content">{{item.description}}</div>

                                                            <span style="font-size: large;">{{item.name}}</span>
                                                        </el-tooltip>
                                                        <span style="font-size: large;" v-else>{{item.name}}</span>
                                                    </el-col>
                                                    <el-button type="info" size="small" icon="el-icon-edit" class="elbtn" @click.stop="openTaskBoxEdit(item)"></el-button>
                                                    <el-button type="danger" size="small" icon="el-icon-delete" class="elbtn" @click.stop="deleteTacsk"></el-button>
                                                </el-row>
                                            </div>
                                            <div style="border-radius: 4px;min-height: 1px;background: #99a9bf;width: 84%;margin: auto"></div>
                                            <el-row>
                                                <el-col :offset="2" style="text-align: left">
                                                    <span style="font-size: initial">{{item.request_header}}</span>
                                                </el-col>
                                            </el-row>
                                        </div>
                                        <div style="min-height: 3px;background: #ffffff"></div>
                                    </li>
                                </ul>

                            </div>
                        </el-scrollbar>
                    </div>
                </el-collapse-transition>

                <div class='popContainer' v-show="taskBox">
                    <div class="taskForm">
                        <el-scrollbar style="height: 100%;">
                            <div style="margin: 30px;font-size: large"><span v-if="this.task_add_or_edit==0">新增任务</span><span v-else-if="this.task_add_or_edit==1">编辑任务</span></div>

                            <el-form ref="taskform" :model="taskform" label-width="80px">
                                <el-row :gutter="10">
                                    <el-col :span="18" :offset="2">
                                        <el-form-item label="任务名称:">
                                            <el-input v-model="taskform.name" size="large" placeholder="请输入任务名称" :disabled=task_add_or_edit></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row :gutter="10">
                                    <el-col :span="18" :offset="2">
                                        <el-form-item label="请求地址:">
                                            <el-input v-model="taskform.request_header" size="large" placeholder="请输入请求地址"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row :gutter="10">
                                    <el-col :span="18" :offset="2">
                                        <el-form-item label="任务描述:">
                                            <el-input type="textarea" :rows="2" placeholder="请输入任务描述" v-model="taskform.description">
                                            </el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-button type="primary" @click="addTask" style="margin: 30px">确定</el-button>

                                <el-button style="margin: 30px" @click="closeTaskBox">取消</el-button>
                            </el-form>
                        </el-scrollbar>
                    </div>
                </div>

                <div class='popContainer' v-show="this.detailTab">
                    <el-scrollbar style="height: 100%;">
                        <div class="detailTable" @mouseleave="closeTab" style="overflow:hidden">

                            <div style="margin-top: 25px;margin-bottom:15px;font-size: large">用例详情</div>
                            <table style="table-layout:fixed;word-break: break-all; word-wrap: break-word;">
                                <tr>
                                    <td class="td1" style="text-align: right">用例编号:</td>
                                    <td style="text-align: left;color: #5b4080;">{{detail.case_id}}</td>
                                    <td class="td1" style="text-align: right">用例名称:</td>
                                    <td style="text-align: left;color: #5b4080;">{{detail.case_name}}</td>
                                    <td class="td1" style="text-align: right">任务名称:</td>
                                    <td style="text-align: left;color: #5b4080;">{{detail.task_name}}</td>
                                    <td class="td1" style="text-align: right">执行结果:</td>
                                    <td style="text-align: left;color: #5b4080;" width="70px">{{detail.actual_result}}</td>
                                </tr>
                                <tr>
                                    <td class="td1" style="text-align: right">请求方法:</td>
                                    <td style="text-align: left;color: #5b4080;">{{detail.method}}</td>
                                    <td class="td1" style="text-align: right">URL:</td>
                                    <td style="text-align: left;color: #5b4080;" colspan="5">{{detail.url}}</td>
                                </tr>
                                <tr>
                                    <td class="td1" style="text-align: right">是否执行:</td>
                                    <td style="text-align: left;color: #5b4080;">{{detail.is_run}}</td>
                                    <td class="td1" style="text-align: right">依赖用例:</td>
                                    <td style="text-align: left;color: #5b4080;" colspan="3">{{detail.dependent_case}}</td>
                                    <td class="td1" style="text-align: right">处理人:</td>
                                    <td style="text-align: left;color: #5b4080;">{{detail.user_name}}</td>
                                </tr>
                                <tr>
                                    <td class="td1" style="text-align: right;">后置处理:</td>
                                    <td style="text-align: left;color: #5b4080;">{{detail.deal_method}}</td>
                                    <td class="td1" style="text-align: right">处理语句:</td>
                                    <td style="text-align: left;color: #5b4080;" colspan="3">{{detail.need_position}}</td>
                                    <td class="td1" style="text-align: right">最新记录:</td>
                                    <td style="text-align: left;color: #5b4080;">{{detail.is_new}}</td>
                                </tr>
                                <tr style="height: 20px;">
                                    <td>提交方式</td>
                                    <td colspan="2">header</td>
                                    <td colspan="5">data</td>
                                </tr>
                                <tr>
                                    <td rowspan="2" style="color: #5b4080;">{{detail.submission}}</td>
                                    <td rowspan="2" colspan="2" style="color: #5b4080;">
                                        <el-scrollbar style="height: 100%">
                                            <div style="height: 70px;">{{detail.header}}</div>
                                        </el-scrollbar>
                                    </td>
                                    <td rowspan="2" colspan="5" style="color: #5b4080;">
                                        <el-scrollbar style="height: 100%">
                                            <div style="width: 96%;height: 70px;">{{detail.data}}</div>
                                        </el-scrollbar>
                                    </td>
                                </tr>
                                <tr>
                                </tr>
                                <tr style="height: 20px;">
                                    <td colspan="3">预期结果</td>
                                    <td colspan="5">接口返回</td>
                                </tr>
                                <tr>
                                    <td rowspan="3" colspan="3" style="color: #5b4080;">{{detail.expect_result}}</td>
                                    <td rowspan="3" colspan="5" style="color: #5b4080;">
                                        <el-scrollbar style="height: 100%">
                                            <div style="width: 96%;height: 70px;">{{detail.interface_return}}</div>
                                        </el-scrollbar>
                                    </td>
                                </tr>

                            </table>
                        </div>
                    </el-scrollbar>
                </div>

                <div class='popContainer' v-show="uploadTask">
                    <div class="taskForm">
                        <div><button class="closebtn" @click="closeUploadBox"><i class="el-icon-close"></i></button></div>
                        <a id="a1" :href="windowUrl + '/v1/interface/downloadTemplet'" target="_blank"></a>
                        <a id="a2" href=""></a>
                        <el-upload class="upload-demo" multiple="" limit="1" ref="uploadExcel" :action="UploadUrl()" :on-success="handleAvatarSuccess" :on-error="handleAvatarError" :on-remove="handleRemove" :on-progress="handleProgress" :on-preview="handlePreview" :file-list="fileList" :auto-upload="false">
                            <div style="margin-top: 35px">
                                <el-button type="primary" @click="downloadTemple">下载模板</el-button>
                                <el-button slot="trigger" type="primary">选取文件</el-button>

                            </div>
                            <div slot="tip" class="el-upload__tip">只能上传excel文件，且不超过5M</div>
                        </el-upload>
                        <el-button style="margin: 20px" type="success" @click="submitUpload">上传任务</el-button>
                        <br />
                        <el-progress v-show="progressShow" width="100" type="circle" :percentage="progressing" :status="progressStatus"></el-progress>

                    </div>
                </div>

                <div id="footer_min" v-if="minWindow"><span>© 2018-2019 automation created by 郭家兴 | 晋ICP备18013433号</span></div>
                <div id="footer" v-else><span>© 2018-2019 automation created by 郭家兴 | 晋ICP备18013433号</span></div>

            </el-main>
        </el-container>
    </div>
</template>
<script>
import VLink from "./VLink.vue";
export default {
  components: {
    VLink
  },
  mounted() {
    const that = this;
        window.onresize = () => {
            return (() => {
                that.screenHeight = window.innerHeight;
            })()
        }
  },
  watch: {
    screenHeight(val){
      if(this.screenHeight<=745){
          this.minWindow = true;
      }else{
          this.minWindow = false;
      }
      
    }
  },
  data() {
    return {
      minWindow: true,
      screenHeight: window.innerHeight,
      activeIndex: "2",
      disabledform: false,
      disabledjson: true,
      detailTab: false,
      fromBox: false,
      taskBox: false,
      leftBox: false,
      hasRun: false,
      uploadTask: false,
      progressShow: false,
      progressStatus: false,
      progressing: 0,
      isActive: 999,
      isSelect: 999,
      task_add_or_edit: 0,
      form_add_or_edit: 0,
      detail: {
        actual_result: "",
        case_id: "dgsdfgs",
        case_name: "",
        data: "",
        deal_method: "",
        dependent_case: "",
        expect_result: "",
        header: "",
        interface_return: "",
        is_new: "",
        is_run: true,
        method: "",
        need_position: "",
        submission: "",
        task_name: "",
        url: "",
        user_name: ""
      },
      pagination: {
        page: 1,
        pages: 0,
        total: 0
      },
      selectTaskId: "",
      searchForm: {
        name: "",
        url: ""
      },
      tableData: [],
      taskform: {
        name: "",
        request_header: "",
        description: ""
      },
      list1: [],
      form: {
        case_id: "",
        case_name: "",
        is_run: true,
        method: "get",
        deal_method: "0",
        url: "",
        header: "",
        /* 提交方式 true json提交，false 表单提交*/
        submission: true,
        need_position: "",
        expect_result: "",
        interfaceReturn: "",
        data: "",
        dependent_case: [],
        options: []
      },
      windowUrl: window.URL
    };
  },
  mounted: function() {
    this.getTask();
    this.getCaseId();
  },
  methods: {
    getCaseId: function() {
      const _self = this;
      $.ajax({
        type: "GET",
        url:
          window.URL +
          "/v1/task/getCaseIdByTaskId?task_id=" +
          _self.selectTaskId,
        contentType: "application/json",
        data: JSON.stringify(this.sendParams),
        success: function(r) {
          _self.form.options = r;
        },
        error: function(r) {}
      });
    },
    /*获取任务列表*/
    getTask: function() {
      const _self = this;
      $.ajax({
        type: "GET",
        url: window.URL + "/v1/task/allTask",
        contentType: "application/json",
        data: JSON.stringify(this.sendParams),
        success: function(r) {
          _self.list1 = r;
        },
        error: function(r) {}
      });
    },
    selectTask(index, itemID) {
      const _self = this;
      this.isSelect = index;
      this.selectTaskId = itemID;
      this.leftBox = false;
      $.ajax({
        type: "GET",
        url: window.URL + "/v1/task/getTaskCase?task_id=" + _self.selectTaskId,
        contentType: "application/json",
        data: JSON.stringify(this.sendParams),
        success: function(r) {
          _self.tableData = r.data;
          _self.pagination.page = r.page;
          _self.pagination.pages = r.pages;
          _self.pagination.total = r.total;
          //刷新用例列表，是否已运行设置为未运行
          _self.hasRun = flase;
        },
        error: function(r) {}
      });
      this.getCaseId();
    },
    handleCurrentChange(currentPage) {
      const _self = this;
      if (this.hasRun == false) {
        $.ajax({
          type: "GET",
          url:
            window.URL +
            "/v1/task/getTaskCase?task_id=" +
            _self.selectTaskId +
            "&page=" +
            currentPage +
            "&case_name=" +
            this.searchForm.name +
            "&url=" +
            this.searchForm.url,
          contentType: "application/json",
          success: function(r) {
            _self.tableData = r.data;
            _self.pagination.page = r.page;
            _self.pagination.pages = r.pages;
            _self.pagination.total = r.total;
          },
          error: function(r) {}
        });
      } else {
        this.sendParams = {
          task_id: this.selectTaskId,
          page: currentPage,
          case_name: this.searchForm.name,
          url: this.searchForm.url
        };
        $.ajax({
          type: "POST",
          url: window.URL + "/v1/interface/searchCase",
          contentType: "application/json",
          data: JSON.stringify(this.sendParams),
          success: function(r) {
            _self.tableData = r.data;
            _self.pagination.page = r.page;
            _self.pagination.pages = r.pages;
            _self.pagination.total = r.total;
          },
          error: function(r) {}
        });
      }
    },
    mouseEnter(index) {
      this.isActive = index;
    },
    mouseLeave() {
      this.isActive = null;
    },
    openError(msg) {
      this.$message.error(msg);
    },
    openWarn(msg) {
      this.$message({
        message: msg,
        type: "warning"
      });
    },
    changeHander(value) {
      if (value == "0") {
        this.disabledform = false;
        this.disabledjson = true;
      } else if (value == "1") {
        this.disabledform = true;
        this.disabledjson = false;
      }
    },
    showCaseDetail: function(row, event) {
      if (this.hasRun == true) {
        const loading = this.$loading({
          lock: true,
          text: "Loading",
          spinner: "el-icon-loading",
          background: "rgba(0, 0, 0, 0.7)",
          target: document.querySelector(".el-container")
        });
        const _self = this;
        $.ajax({
          type: "GET",
          url: window.URL + "/v1/interface/getCaseDetail?id=" + row.id,
          contentType: "application/json",
          success: function(r) {
            _self.detail = r;
            if (r.actual_result == "1") {
              _self.detail.actual_result = "通过";
            } else {
              _self.detail.actual_result = "失败";
            }
            if (r.deal_method == "0") {
              _self.detail.deal_method = "不做处理";
            } else if (r.deal_method == "1") {
              _self.detail.deal_method = "默认处理";
            } else if (r.deal_method == "2") {
              _self.detail.deal_method = "获取key值存储";
            } else {
              _self.detail.deal_method = "正则表达式";
            }
            if (r.is_new == true) {
              _self.detail.is_new = "是";
            } else {
              _self.detail.is_new = "否";
            }
            if (r.is_run == true) {
              _self.detail.is_run = "是";
            } else {
              _self.detail.is_run = "否";
            }
            if (r.submission == "0") {
              _self.detail.submission = "表单提交";
            } else {
              _self.detail.submission = "json提交";
            }
            try {
              if (r.interface_return) {
                _self.detail.interface_return = JSON.stringify(
                  JSON.parse(r.interface_return),
                  null,
                  2
                );
              }
            } catch (e) {}
            if (r.data) {
              _self.detail.data = JSON.stringify(JSON.parse(r.data), null, 2);
            }
            if (r.header) {
              _self.detail.header = JSON.stringify(
                JSON.parse(r.header),
                null,
                2
              );
            }

            loading.close();
          },
          error: function(r) {
            if (r.responseJSON.error_code) {
              loading.close();
              _self.openError("未查询到明细");
            }
          }
        });

        this.detailTab = true;
      }
    },
    openTaskBox: function() {
      this.taskBox = true;
      this.leftBox = false;
      this.task_add_or_edit = 0;
    },
    openTaskBoxEdit: function(item) {
      this.taskBox = true;
      this.leftBox = false;
      this.task_add_or_edit = 1;
      this.taskform.name = item.name;
      this.taskform.request_header = item.request_header;
      this.taskform.description = item.description;
      this.rotationButton();
    },
    openFormBox: function() {
      this.fromBox = true;
      this.form_add_or_edit = 0;
    },
    UploadUrl: function() {
      return window.URL + "/v1/interface/upload";
    },
    deleteTacsk: function() {
      this.$confirm("此操作将永久删除该任务, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          this.$message({
            message: "您无此操作权限，请联系管理员提升权限",
            type: "warning"
          });
        })
        .catch(() => {});
    },
    deleteTaskCase: function(index, row) {
      this.$confirm("此操作将永久删除该用例, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          const loading = this.$loading({
            lock: true,
            text: "Loading",
            spinner: "el-icon-loading",
            background: "rgba(0, 0, 0, 0.7)",
            target: document.querySelector(".el-container")
          });
          const _self = this;
          $.ajax({
            type: "GET",
            url: window.URL + "/v1/task/deleteTaskCase?case_id=" + row.case_id,
            contentType: "application/json",
            data: JSON.stringify(this.sendParams),
            success: function(r) {
              loading.close();
              _self.$alert("删除成功！", "提示", {
                confirmButtonText: "确定",
                callback: action => {
                  this.$message({
                    type: "info",
                    message: `action: ${action}`
                  });
                }
              });
              $.ajax({
                type: "GET",
                url:
                  window.URL +
                  "/v1/task/getTaskCase?task_id=" +
                  _self.selectTaskId,
                contentType: "application/json",
                data: JSON.stringify(this.sendParams),
                success: function(r) {
                  _self.tableData = r.data;
                  _self.pagination.page = r.page;
                  _self.pagination.pages = r.pages;
                  _self.pagination.total = r.total;
                  //刷新用例列表，是否已运行设置为未运行
                  _self.hasRun = false;
                },
                error: function(r) {}
              });
              _self.getCaseId();
            },
            error: function(r) {
              if (r.responseJSON.error_code) {
                loading.close();
                if (r.responseJSON.error_code == 1016) {
                  _self.openWarn("该用例已被依赖，请解除依赖关系后重试");
                } else if (r.responseJSON.error_code == 1004) {
                  _self.openWarn("您无此操作的权限，请联系管理员升级权限");
                } else {
                  _self.openError("系统错误请重试");
                }
              }
            }
          });
        })
        .catch(() => {});
    },
    upLoad: function() {
      this.uploadTask = true;
    },
    openFormBoxEdit: function(index, row) {
      this.fromBox = true;
      this.form_add_or_edit = 1;
      const _self = this;
      $.ajax({
        type: "GET",
        url:
          window.URL +
          "/v1/task/getTaskCase?task_id=" +
          _self.selectTaskId +
          "&case_id=" +
          row.case_id,
        contentType: "application/json",
        data: JSON.stringify(this.sendParams),
        success: function(r) {
          _self.form.case_id = r.case_id;
          _self.form.case_name = r.case_name;
          _self.form.is_run = r.is_run;
          _self.form.method = r.method;
          _self.form.url = r.url;
          _self.form.header = r.header;
          _self.form.deal_method = r.deal_method;
          if (r.dependent_case == "") {
            _self.form.dependent_case = [];
          } else {
            _self.form.dependent_case = r.dependent_case.split(",");
          }
          _self.form.need_position = r.need_position;
          _self.form.data = r.data;
          if (r.submission == "1") {
            _self.form.submission = true;
          } else if (r.submission == "0") {
            _self.form.submission = false;
          }
          _self.form.expect_result = r.expect_result;
        },
        error: function(r) {
          if (r.responseJSON.error_code) {
            loading.close();
            _self.openError("系统错误请重试");
          }
        }
      });
    },
    closeTab: function() {
      this.detailTab = false;
    },
    closeTaskBox: function() {
      this.taskBox = false;
      this.taskform.name = "";
      this.taskform.request_header = "";
      this.taskform.description = "";
    },
    closeFormBox: function() {
      this.fromBox = false;
      (this.form.case_id = ""),
        (this.form.case_name = ""),
        (this.form.is_run = true),
        (this.form.method = "get"),
        (this.form.url = ""),
        (this.form.header = ""),
        (this.form.deal_method = "0"),
        (this.form.dependent_case = []),
        (this.form.need_position = ""),
        (this.form.data = ""),
        (this.form.submission = ""),
        (this.form.expect_result = "");
    },
    addEditCase: function() {
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
        target: document.querySelector(".el-container")
      });
      if (this.form.submission == true) {
        this.form.submission = "1";
      } else if (this.form.submission == false) {
        this.form.submission = "0";
      }
      this.sendParams = {
        case_id: this.form.case_id,
        case_name: this.form.case_name,
        is_run: this.form.is_run,
        method: this.form.method,
        url: this.form.url,
        header: this.form.header,
        deal_method: this.form.deal_method,
        dependent_case: this.form.dependent_case.join(),
        need_position: this.form.need_position,
        data: this.form.data,
        submission: this.form.submission,
        expect_result: this.form.expect_result,
        task_id: this.selectTaskId
      };
      const _self = this;
      if (this.form_add_or_edit == 0) {
        $.ajax({
          type: "POST",
          url: window.URL + "/v1/task/addTaskCase",
          contentType: "application/json",
          data: JSON.stringify(this.sendParams),
          success: function(r) {
            loading.close();
            _self.closeFormBox();
            _self.$alert("新增成功！", "提示", {
              confirmButtonText: "确定",
              callback: action => {
                this.$message({
                  type: "info",
                  message: `action: ${action}`
                });
              }
            });
            $.ajax({
              type: "GET",
              url:
                window.URL +
                "/v1/task/getTaskCase?task_id=" +
                _self.selectTaskId,
              contentType: "application/json",
              data: JSON.stringify(this.sendParams),
              success: function(r) {
                _self.tableData = r.data;
                _self.pagination.page = r.page;
                _self.pagination.pages = r.pages;
                _self.pagination.total = r.total;
              },
              error: function(r) {}
            });
            _self.getCaseId();
          },
          error: function(r) {
            console.log(r);
            if (r.responseJSON.error_code) {
              loading.close();
              if (r.responseJSON.error_code == 1000) {
                _self.openWarn("用例名称、URL不能为空");
              } else {
                _self.openError("输入数据有误请重新输入");
              }
            }
            console.log(r);
            console.log(12);
          }
        });
      } else if (this.form_add_or_edit == 1) {
        $.ajax({
          type: "POST",
          url: window.URL + "/v1/task/updateTaskCase",
          contentType: "application/json",
          data: JSON.stringify(this.sendParams),
          success: function(r) {
            loading.close();
            _self.closeFormBox();
            _self.$alert("编辑成功！", "提示", {
              confirmButtonText: "确定",
              callback: action => {
                this.$message({
                  type: "info",
                  message: `action: ${action}`
                });
              }
            });
            $.ajax({
              type: "GET",
              url:
                window.URL +
                "/v1/task/getTaskCase?task_id=" +
                _self.selectTaskId + "&page=" + _self.pagination.page,
              contentType: "application/json",
              data: JSON.stringify(this.sendParams),
              success: function(r) {
                _self.tableData = r.data;
                _self.pagination.page = r.page;
                _self.pagination.pages = r.pages;
                _self.pagination.total = r.total;
              },
              error: function(r) {}
            });
            _self.getCaseId();
          },
          error: function(r) {
            console.log(r);
            if (r.responseJSON.error_code) {
              loading.close();
              if (r.responseJSON.error_code == 1000) {
                _self.openWarn("任务名称 URL不能为空");
              } else {
                _self.openError("输入数据有误请重新输入");
              }
            }
            console.log(r);
            console.log(12);
          }
        });
      }
      //刷新用例列表，是否已运行设置为未运行
      this.hasRun = false;
    },
    addTask: function() {
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
        target: document.querySelector(".el-container")
      });
      this.sendParams = {
        name: this.taskform.name,
        request_header: this.taskform.request_header,
        description: this.taskform.description
      };
      const _self = this;
      if (this.task_add_or_edit == 0) {
        $.ajax({
          type: "POST",
          url: window.URL + "/v1/task/addTask",
          contentType: "application/json",
          data: JSON.stringify(this.sendParams),
          success: function(r) {
            console.log(r);
            _self.getTask();
            loading.close();
            _self.closeTaskBox();
            _self.$alert("新增成功！", "提示", {
              confirmButtonText: "确定",
              callback: action => {
                this.$message({
                  type: "info",
                  message: `action: ${action}`
                });
              }
            });
          },
          error: function(r) {
            console.log(r);
            if (r.responseJSON.error_code) {
              loading.close();
              if (r.responseJSON.error_code == 1000) {
                _self.openWarn("任务名称不能为空");
              } else if (r.responseJSON.error_code == 1010) {
                _self.openWarn("任务名称已经存在请重新输入");
              } else {
                _self.openError("输入数据有误请重新输入");
              }
            }
            console.log(r);
            console.log(12);
          }
        });
      } else if (this.task_add_or_edit == 1) {
        $.ajax({
          type: "POST",
          url: window.URL + "/v1/task/updateTask",
          contentType: "application/json",
          data: JSON.stringify(this.sendParams),
          success: function(r) {
            console.log(r);
            _self.getTask();
            loading.close();
            _self.closeTaskBox();
            _self.$alert("编辑成功！", "提示", {
              confirmButtonText: "确定",
              callback: action => {
                this.$message({
                  type: "info",
                  message: `action: ${action}`
                });
              }
            });
          },
          error: function(r) {
            console.log(r);
            if (r.responseJSON.error_code) {
              loading.close();
              if (r.responseJSON.error_code == 1000) {
                _self.openWarn("任务名称不能为空");
              } else {
                _self.openError("输入数据有误请重新输入");
              }
            }
            console.log(r);
            console.log(12);
          }
        });
      }
    },
    downloadTemple: function() {
      document.getElementById("a1").click();
    },
    submitUpload: function() {
      this.progressShow = true;
      this.$refs.uploadExcel.submit();
    },
    send: function() {
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
        target: document.querySelector(".el-container")
      });
      this.sendParams = {
        task_id: this.selectTaskId
      };
      const _self = this;
      $.ajax({
        type: "POST",
        url: window.URL + "/v1/interface/spider/batch",
        contentType: "application/json",
        data: JSON.stringify(this.sendParams),
        success: function(r) {
          _self.hasRun = true;
          this.sendParams = _self.sendParams;
          $.ajax({
            type: "POST",
            url: window.URL + "/v1/interface/searchCase",
            contentType: "application/json",
            data: JSON.stringify(this.sendParams),
            success: function(r) {
              _self.tableData = r.data;
              _self.pagination.page = r.page;
              _self.pagination.pages = r.pages;
              _self.pagination.total = r.total;
            },
            error: function(r) {}
          });
          loading.close();
          _self.$notify({
            title: "已完成",
            duration: 0,
            type: "success",
            dangerouslyUseHTMLString: true,
            message:
              "任务共<strong>" +
              r.total +
              "</strong>条<br>此次执行<strong>" +
              r.has_run +
              "</strong>条<br>成功<strong>" +
              r.pass_num +
              '</strong>条<br>失败<strong><span style="color: #ff1d06;">' +
              r.fail_num +
              "</span></strong>条"
          });
        },
        error: function(r) {
          console.log(r);
          if (r.responseJSON.error_code) {
            loading.close();
            if (r.responseJSON.error_code == 1000) {
              _self.openWarn("用例名称或url不能为空");
            } else {
              _self.openError("数据有误请编辑后重试！");
            }
          }
        }
      });
    },
    handleProgress() {
      var _this = this;
      clearInterval(this.time);
      this.time = setInterval(function() {
        if (_this.progressing < 100) {
          _this.progressing += 10; //进程条
        } else {
        }
      }, 500);
    },
    handleAvatarError(err, file) {
      clearInterval(this.time);
      this.progressStatus = "exception";
      console.log(err.message);

      if (
        err.message ==
        '{"error_code": 1018, "msg": "data is not null", "request": "POST /v1/interface/upload"}'
      ) {
        this.openWarn("任务名称不能为空");
      }
    },
    handleAvatarSuccess(res, file) {
      this.progressing = 100;
      clearInterval(this.time);
      this.progressStatus = "success"; //进程状态
      var _this = this;
      setTimeout(function() {
        _this.showFlag = false;
      }, 2000);
      this.getTask();
    },
    handleRemove() {
      this.progressing = 0;
      this.progressStatus = false;
      this.progressShow = false;
    },
    filterTag(value, row) {
      return row.actual_result === value;
    },
    closeUploadBox() {
      this.uploadTask = false;
      this.handleRemove();
    },
    rowStyle(val) {
      if (this.hasRun == true) {
        return "cursor: pointer";
      } else {
        return "";
      }
    },
    rotationButton() {
      var rotationB = document.getElementById("rotation");
      var deg = rotationB.style.transform;
      deg = deg.replace(/[^0-9]/gi, "");
      deg = Number(deg);
      console.log(deg);
      var step = 180;
      rotationB.style.transform = "rotate(" + (deg + step) + "deg)";
    },
    openFullScreen() {
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)"
      });
      setTimeout(() => {
        loading.close();
      }, 5000);
    }
  }
};
</script>

<style scoped>
#app {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  text-align: center;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
}
#table {
  display: inline-block;
  margin-top: 25px;
}
.el-scrollbar__wrap {
  overflow-x: hidden;
}

.el-row {
  padding-top: 15px;
  margin-left: 0 !important ;
  margin-right: 0 !important ;
}

.grid-content2 {
  border-radius: 6px;
  min-height: 6px;
  background: #409eff;
}

.grid-content {
  border-radius: 4px;
  min-height: 3px;
  background: #99a9bf;
  width: 97%;
  margin: 0 auto;
}

.box {
  border-radius: 4px;
  background-color: #409eff;
  text-align: center;
  color: #fff;
  box-sizing: border-box;
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
  display: flex;
  justify-content: center;
}
#footer_min {
  color: #9a9b9c;
  font-weight: 400;
  margin-top: 10px;
  margin-bottom: 15px;
  width: 97%;
  display: flex;
  justify-content: center;
}
.elbtn {
  margin: 0;
}
[v-cloak] {
  display: none;
}
.el-col {
  height: 40px;
}
div.popContainer {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
}
div.popContainer2 {
  position: fixed;
  top: 143px;
  left: 0;
  width: 350px;
  bottom: 70px;
  background: rgba(255, 255, 255, 0.9);
}
.caseForm {
  width: 55%;
  height: 70%;
  overflow: auto;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  background: #ffffff;
}
.taskForm {
  width: 30%;
  height: 49%;
  overflow: auto;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 25%;
  right: 0;
  background: #ffffff;
}
.detailTable {
  width: 60%;
  height: 75%;
  overflow: auto;
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  background: #ffffff;
}
ul,
li {
  list-style: none;
  margin: 0px;
  padding: 0px;
  cursor: pointer;
}
.el-menu-item {
  padding: 0 20px;
}
.active {
  background: rgba(1, 144, 254, 0.51);
  color: #fff;
}
.select {
  background: rgb(1, 144, 254);
  color: #fff;
}
.el-table th {
  -moz-user-select: none;
  text-align: center !important;
}
.el-table__column-filter-trigger i {
  color: #f2f6fc;
  font-size: 17px;
}
.el-icon-arrow-down {
  color: #ecf5ff;
}
.el-table th > .cell.highlight {
  color: #ecf5ff;
}
.el-table__column-filter-trigger {
  display: inline-block;
  line-height: 23px;
  cursor: pointer;
}
.detailTable table,
th,
td {
  border: 1px solid #ebeef5;
  border-collapse: collapse;
}
.detailTable table {
  width: 85%;
  height: 80%;
  margin: auto;
}
.td1 {
  border-right-style: none;
  width: 85px;
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
.el-header {
  padding: 0;
}

.el-main {
  padding: 10px;
}

.el-container {
  height: 100%;
}
#rotation{
  
}
</style>
