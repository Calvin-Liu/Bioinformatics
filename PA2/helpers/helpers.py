import numpy as np

def read_reads(read_fn):
    f = open(read_fn, 'r')
    first_line = True
    all_reads = []
    for line in f:
        if first_line:
            first_line = False
            continue  # We skip the first line, since it
            # only contains the name of the chromosome the reads
            # came from.
        line = line.strip()
        paired_end_reads = line.split(',')  # The two paired ends are separated by a comma
        all_reads.append(paired_end_reads)
    return all_reads


def read_reference(ref_fn):
    f = open(ref_fn, 'r')
    first_line = True
    output_reference = ''
    for line in f:
        if first_line:
            first_line = False
            continue  # We skip the first line, since it
            # only contains the name of the chromosome the reads
            # came from.
        line = line.strip()
        output_reference += line  # We append each line to the output reference string.
    return output_reference


def pretty_print_aligned_reads_with_ref(genome_oriented_reads, read_alignments, ref):
    """
    :param genome_oriented_reads: oriented reads generated by trivial_algorithm
    :param read_alignments: alignments generated from trivial_algorithm
    :param ref: reference generated by read_ref
    :return: Returns nothing, but prints the reads aligned to the genome to
     show you what pileup actually *LOOKS* like. You should be able to call SNPs
     by eyeballing the output. However, there are some reads that will not align.
     In the future you'll want to re-check why these reads aren't aligning--the cause
     is usually a structural variation, like an insertion or deletion.
    """
    output_string = ''
    good_alignments = [x != -1 for x in read_alignments]
    # There should be 50 + x (90 < x < 110) p between the reads, and we give a little
    # extra space in case there's been a deletion or insertion.  Depending on the type of
    # deletions/insertions

    good_reads = [genome_oriented_reads[i] for i in range(len(good_alignments))
                  if good_alignments[i]]
    # Remove the reads that do not have a good alignment, or a good reverse alignment.
    good_alignment_locations = [read_alignments[i] for i in range(len(read_alignments))
                                if good_alignments[i]]
    # Take their corresponding alignments
    # This turns the reads into strings oriented towards the genome.
    # We get the first read, followed by the correct number of dots to join the first and second reads,
    # and then the second read.

    alignment_indices = np.argsort(good_alignment_locations)
    sorted_reads = [good_reads[i] for i in alignment_indices]
    sorted_alignments = [good_alignment_locations[i] for i in alignment_indices]

    # You don't need to worry too much about how the code block below works--its job is to make it so
    # that a read that starts printing in the third row will continue printing in the third row of the
    # next set of lines.
    active_reads = []
    line_length = 100
    output_string += '\n\n' + '-' * (line_length + 6) + '\n\n'
    for i in range(len(ref) / line_length):
        next_ref = ref[i * line_length: (i + 1) * line_length]
        new_read_indices = [j for j in range(len(sorted_reads))
                            if i * line_length <= sorted_alignments[j] < (i + 1) * line_length]
        space_amounts = [sorted_alignments[index] % line_length for index in new_read_indices]
        new_reads = [sorted_reads[index] for index in new_read_indices]
        new_reads_with_spaces = [' ' * space_amounts[j] + new_reads[j] for j in range(len(new_reads))]
        empty_active_read_indices = [index for index in range(len(active_reads)) if active_reads[index] == '']
        for j in range(min(len(new_reads_with_spaces), len(empty_active_read_indices))):
            active_reads[empty_active_read_indices[j]] = new_reads_with_spaces[j]

        if len(new_reads_with_spaces) > len(empty_active_read_indices):
            active_reads += new_reads_with_spaces[len(empty_active_read_indices):]
        printed_reads = ['Read: ' + read[:line_length] for read in active_reads]
        active_reads = [read[line_length:] for read in active_reads]
        while len(active_reads) > 0:
            last_thing = active_reads.pop()
            if last_thing != '':
                active_reads.append(last_thing)
                break
        output_lines = ['Ref:  ' + next_ref] + printed_reads
        output_string += 'Reference index: ' + str(i * line_length) + \
                         '\n' + '\n'.join(output_lines) + '\n\n' + '-' * (line_length + 6) + '\n\n'
    return output_string