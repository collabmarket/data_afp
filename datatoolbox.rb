require 'fileutils'

def logg_info(msg, tipo='INFO', status='OK')
    timestamp = Time.now.strftime('%Y-%m-%d %H:%M:%S')
    puts "[#{tipo}]--#{timestamp}--#{msg}--#{status}"
end

def makedir(dirname, by=File.basename(__FILE__))
    if not File.exist?(dirname)
        FileUtils.mkdir(dirname)
        logg_info("#{by} mkdir #{dirname}", tipo='INFO', status='OK')
    end
end
