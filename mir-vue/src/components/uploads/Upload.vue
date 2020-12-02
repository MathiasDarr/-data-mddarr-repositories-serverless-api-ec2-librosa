<template>
 <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>File
        <input type="file" id="file" ref="file" v-on:change="onFileChange()"/>
      </label>
    </div>
  </div>
</template>


<script>
/* eslint-disable */


export default {
  props: ['files'],
  data () {
    return {
      file: ''
    }
  },
  methods: {
      upload(){
        var albumBucketName = "BUCKET_NAME";
        var bucketRegion = "us-west-2";
        var IdentityPoolId = "IDENTITY_POOL_ID";

        AWS.config.update({
            region: bucketRegion,
                credentials: new AWS.CognitoIdentityCredentials({
                IdentityPoolId: IdentityPoolId
            })
        });

        var s3 = new AWS.S3({
            apiVersion: "2006-03-01",
            params: { Bucket: albumBucketName }
        });
      },


      onFileChange(){
        this.file = this.$refs.file.files[0];
      if (this.file) {
          this.$store.dispatch('upload/fetchSignatureAndPolicy', {
            name: this.file.name,
            type: this.file.type
          }).then(() => {
            let policy = this.$store.state.upload.policy
            var formData = new FormData()
            formData.append('key', policy.key)
            formData.append('acl', policy.acl)
            formData.append('Content-Type', this.file.type)
            formData.append('success_action_status', policy.success_action_status)
            formData.append('policy', policy.policy)
            formData.append('x-amz-credential', policy['x-amz-credential'])
            formData.append('x-amz-algorithm', policy['x-amz-algorithm'])
            formData.append('x-amz-date', policy['x-amz-date'])
            formData.append('x-amz-security-token', policy['x-amz-security-token'])
            formData.append('x-amz-signature', policy['x-amz-signature'])
            formData.append('file', this.file)
            this.$store.dispatch('upload/upload', formData).then((data) => {
            })
          })
        }
      }
   },
}
</script>