module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      build: {
        src: 'src/<%= pkg.name %>.js',
        dest: 'build/<%= pkg.name %>.min.js'
      }
    },
    bower_concat: {
      all: {
        dest: 'static/build/js/internwatch.js',
        cssDest: 'static/build/css/internwatch.css',
        exclude: [
          //'jquery',
          //'modernizr'
        ],
        bowerOptions: {
          relative: false
        }
      }
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-bower-concat');

  // Default task(s).
  //grunt.registerTask('default', ['uglify']);

  grunt.registerTask('default', ['bower_concat']);
};
