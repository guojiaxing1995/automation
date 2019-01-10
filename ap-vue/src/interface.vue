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

        <el-form ref="form" :model="form" label-width="80px">
          <el-row :gutter="20">
            <el-col :span="5" :offset="6">
              <el-form-item label="用例名称:">
                <el-input v-model="form.name" size="large" placeholder="请输入用例名称"></el-input>
              </el-form-item>

            </el-col>
            <el-col :span="4" :offset="1">
              <el-form-item label="请求方式:" :value="form.methods">
                <el-select v-model="form.methods">
                  <el-option label="GET" value="get" selected="selected"></el-option>
                  <el-option label="POST" value="post"></el-option>
                  <el-option label="PUT" value="put"></el-option>
                  <el-option label="DELETE" value="delete"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="10" :offset="6">
              <el-form-item label="URL:">
                <el-input v-model="form.url" placeholder="请输入请求地址"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="2" :offset="1">
              <el-button type="primary" size="medium" @click="send" style="font-weight:500"> SEND</el-button>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="6" :offset="1">
              <el-form-item label="header:">
                <el-input type="textarea" :rows="5" placeholder="请输入请求参数" v-model="form.header">
                </el-input>
              </el-form-item>
            </el-col>
            <el-radio-group v-model="form.radio" size="small" @change="changeHander">
              <el-col :span="3" offset="1">
                <el-radio label="0" border>form提交</el-radio>
              </el-col>
              <el-col :span="7">
                <!-- <el-form-item label="form提交:" > -->
                <el-input type="textarea" :rows="5" placeholder="请输入请求参数" :disabled="disabledform" v-model="form.formData">
                </el-input>
                <!-- </el-form-item> -->
              </el-col>
              <el-col :span="3" offset="1">
                <el-radio label="1" border>json提交</el-radio>
              </el-col>
              <el-col :span="7">
                <!-- <el-form-item label="json提交:"  > -->
                <el-input type="textarea" :rows="5" placeholder="请输入请求参数" :disabled="disabledjson" v-model="form.jsonData">
                </el-input>
                <!-- </el-form-item> -->
              </el-col>
            </el-radio-group>

          </el-row>
          <el-row>
            <el-col :span="22" offset="1">
              <div class="grid-content"></div>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="6" :offset="4">
              <div class="box" style="font-weight:500">预期结果</div>
              <el-input type="textarea" :rows="10" placeholder="" v-model="form.expectResult">
              </el-input>
            </el-col>
            <el-col :span="6" :offset="1">
              <div class="box" style="font-weight:500">接口返回</div>
              <el-input type="textarea" :rows="10" readonly=true placeholder="" v-model="form.interfaceReturn">
              </el-input>
            </el-col>
            <el-col :span="1" :offset="2">

              <div v-cloak>
                <transition name="el-zoom-in-center">
                  <div v-show="form.actualResultPass" class="transitionPass-box">pass</div>
                </transition>
                <transition name="el-zoom-in-center">
                  <div v-show="form.actualResultFail" class="transitionFail-box">fail</div>
                </transition>
              </div>
              <!-- <el-tag type="success" v-show="form.actualResultPass">pass</el-tag>
                        <el-tag type="success" v-show="form.actualResultFail">fail</el-tag> -->
            </el-col>
          </el-row>

        </el-form>
        <div id="footer" class="flex-hor-center">
          <span>© 2018-2019 automation created by 郭家兴 | 晋ICP备18013433号</span>
        </div>
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
  data() {
    return {
      activeIndex: "1",
      disabledform: false,
      disabledjson: true,
      form: {
        name: "",
        methods: "get",
        url: "",
        header: "",
        formData: "",
        jsonData: "",
        expectResult: "",
        interfaceReturn: "",
        actualResultPass: false,
        actualResultFail: false,
        radio: "0",
        data: ""
      }
    };
  },
  methods: {
    go() {},
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
    send: function() {
      const loading = this.$loading({
        lock: true,
        text: "Loading",
        spinner: "el-icon-loading",
        background: "rgba(0, 0, 0, 0.7)",
        target: document.querySelector(".el-container")
      });
      if (this.form.radio == "0") {
        this.form.data = this.form.formData;
      } else if (this.form.radio == "1") {
        this.form.data = this.form.jsonData;
      }
      this.sendParams = {
        case_name: this.form.name,
        method: this.form.methods,
        url: this.form.url,
        data: this.form.data,
        submission: this.form.radio,
        header: this.form.header,
        expect_result: this.form.expectResult
      };
      const _self = this;
      $.ajax({
        type: "POST",
        url: window.URL + "/v1/interface/spider",
        contentType: "application/json",
        data: JSON.stringify(this.sendParams),
        success: function(r) {
          console.log(r);
          _self.form.name = r.case_name;
          _self.form.methods = r.expect_result;
          _self.form.url = r.url;
          _self.form.radio = r.submission;
          _self.form.data = r.data;
          if (_self.form.data) {
            _self.form.data = JSON.stringify(
              JSON.parse(_self.form.data),
              null,
              2
            );
          }
          if (r.submission == "0") {
            _self.form.formData = _self.form.data;
          } else if (r.submission == "1") {
            _self.form.jsonData = _self.form.data;
          }
          _self.form.header = r.header;
          _self.form.expectResult = r.expect_result;
          if (r.interface_return) {
            r.interface_return = JSON.stringify(
              JSON.parse(r.interface_return),
              null,
              2
            );
          }
          _self.form.interfaceReturn = r.interface_return;
          _self.form.methods = r.method;
          loading.close();

          setTimeout(
            new Function((_self.form.actualResultPass = r.actual_result))(),
            0
          );
          setTimeout(
            new Function((_self.form.actualResultFail = !r.actual_result))(),
            0
          );
        },
        error: function(r) {
          console.log(r);
          if (r.responseJSON.error_code) {
            loading.close();
            if (r.responseJSON.error_code == 1000) {
              _self.openWarn("用例名称或url不能为空");
            } else {
              _self.openError("输入数据有误请重新输入");
            }
          }
          console.log(r);
          console.log(12);
        }
      });
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
  font-weight: 600;
  text-align: center;
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
}
.el-menu{
  font-weight: 500;
}
.el-row {
  padding-top: 20px;
}

.grid-content {
  border-radius: 4px;
  min-height: 5px;
  background: #99a9bf;
  margin-bottom: 1%;
}

.el-tag--success {
  height: 60px;
  text-align: center;
  width: 160px;
  font-size: 50px;
  margin-top: 50px;
}

.box {
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  border-bottom-left-radius: 0px;
  border-bottom-right-radius: 0;
  background-color: #409eff;
  text-align: center;
  color: #fff;
  box-sizing: border-box;
}

.transitionPass-box {
  margin-top: 50px;
  width: 150px;
  height: 100px;
  border-radius: 4px;
  background-color: #67c23a;
  text-align: center;
  color: #fff;
  padding: 30px 20px;
  box-sizing: border-box;
  font-size: 30px;
}

.el-radio-group {
  width: 66.5%;
}
.el-radio {
  font-weight: 700;
}
.transitionFail-box {
  margin-top: 50px;
  width: 150px;
  height: 100px;
  border-radius: 4px;
  background-color: #f56c6c;
  text-align: center;
  color: #fff;
  padding: 30px 20px;
  box-sizing: border-box;
  font-size: 30px;
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

[v-cloak] {
  display: none;
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
</style>