package com.rockit.nesoi;


import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Created by brlamore on 11/23/15.
 */
public class AssignBounds {

    public static class BoundsMapper  extends Mapper<Object, Text, Text, IntWritable>{

        private Logger logger = LoggerFactory.getLogger(BoundsMapper.class);

        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {

            logger.debug("In Mapper bb");


            context.write(new Text(value + ",55"), one);

//            StringTokenizer itr = new StringTokenizer(value.toString());
//            while (itr.hasMoreTokens()) {
//                word.set(itr.nextToken());
//                context.write(word, one);
//            }
        }
    }

    public static class IntSumReducer extends Reducer<Text,IntWritable,Text,IntWritable> {

        private Logger logger = LoggerFactory.getLogger(IntSumReducer.class);

        private IntWritable result = new IntWritable(1);

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {

            logger.debug("In Reducer");

            Text t = new Text("where");
//            int sum = 0;
            for (IntWritable val : values) {
                logger.debug(val.toString());
            }
//
//            if(key.equals(t)){
//                result.set(999);
//            }
//            else {
//                result.set(sum);
//            }

//            result.set(999);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "assign bounds");
        job.setJarByClass(AssignBounds.class);
        job.setMapperClass(BoundsMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }

}
