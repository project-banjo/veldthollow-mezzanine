module.exports = (grunt) ->
    grunt.initConfig
        pkg: grunt.file.readJSON 'package.json'
        stylus:
            compile:
                options:
                    compress: false
                files:
                    'tmp/main.css': 'customizations/media/styles/**/*.styl'
                    'tmp/splash.css': 'customizations/media/styles/splash/*.styl'
        #coffee:
        #    compile:
        #        files:
        #            'tmp/podcast_client.js': 'scripts/**/*.coffee'
        uglify:
            scripts:
                files:
                    'customizations/static/js/main.js': [
                        'scripts/vendor/bootstrap.min.js'
                        #'tmp/podcast_client.js'
                    ]
        concat:
            styles:
                files:
                    'customizations/static/css/main.css': [
                        'tmp/main.css'
                    ]
                    'customizations/static/css/splash.css': [
                        'tmp/splash.css'
                    ]
        watch:
            #coffee:
            #    files: 'scripts/**/*.coffee'
            #    tasks: ['coffee', 'uglify:scripts']
            js:
                files: 'customizations/media/scripts/**/*.js'
                tasks: ['uglify:scripts']
            stylus:
                files: 'customizations/media/styles/**/*.styl'
                tasks: ['stylus', 'concat:styles']
            css:
                files: 'customizations/media/styles/**/*.css'
                tasks: ['concat:styles']

    grunt.loadNpmTasks 'grunt-contrib-uglify'
    grunt.loadNpmTasks 'grunt-contrib-concat'
    #grunt.loadNpmTasks 'grunt-contrib-coffee'
    grunt.loadNpmTasks 'grunt-contrib-stylus'
    grunt.loadNpmTasks 'grunt-contrib-watch'

    grunt.registerTask 'default', ['stylus', 'concat', 'uglify'] #'coffee', 'uglify']
    grunt.registerTask 'w', ['default', 'watch']

