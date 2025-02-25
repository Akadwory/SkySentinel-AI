import pandas as pd 


input_file_path = '/Users/adamkadwory/Desktop/skysentineAI/data/flight_data_1.0.csv'
output_file_path = '/Users/adamkadwory/Desktop/skysentineAI/data/sampled_flight_data.csv'


#Sampling Configuration 
chunk_size = 100000 #adjust based on the capacity of the system 
sample_fraction = 0.01 #modify based on how much sample we add 

# Open the output file for writing (overwriting existing file)
with open(output_file_path,'w') as output_file:
    write_header = True  #ensure we only write the header once 

    #process and sample each chunk 
    for chunk in pd.read_csv(input_file_path,chunksize=chunk_size):
        sampled_chunk = chunk.sample(frac = sample_fraction)

        #Append samples to the file 
        sampled_chunk.to_csv(output_file, mode = 'a', index=False, header=write_header)
        write_header = False #disable the header after writing 

print(f"Sampled data saved and updated in-place to: {output_file_path}")

