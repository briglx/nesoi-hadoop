import java.io.IOException;
import java.util.Arrays;

import com.rockit.nesoi.AssignBounds;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mrunit.mapreduce.MapDriver;
import org.apache.hadoop.mrunit.mapreduce.ReduceDriver;
import org.junit.*;

/**
 * Created by brlamore on 11/30/15.
 */
public class AssignBoundsMapperTest {

    @Test
    public void processesValidRecord() throws IOException, InterruptedException {

        Text value = new Text("1,0,mountainGreen,false");

        new MapDriver<Object, Text, Text, IntWritable>()
                .withMapper(new AssignBounds.BoundsMapper())
                .withInput(new LongWritable(0), value)
                .withOutput(new Text("1,0,mountainGreen,false,55"), new IntWritable(1))
                .runTest();
    }

    @Test
    public void returnsMaximumIntegerInValues() throws IOException,
            InterruptedException {
        new ReduceDriver<Text, IntWritable, Text, IntWritable>()
                .withReducer(new AssignBounds.IntSumReducer())
                .withInput(new Text("1,0,mountainGreen,false,55"),
                        Arrays.asList(new IntWritable(1)))
                .withOutput(new Text("1,0,mountainGreen,false,55"), new IntWritable(1))
                .runTest();
    }


}
