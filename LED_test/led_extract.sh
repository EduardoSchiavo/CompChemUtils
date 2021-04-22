#!/bin/bash

echo "E(HF):" 
grep "E(0)" *.out
echo "Ec(CCSD):"
grep "E(CORR)(corrected)" *.out
echo "Ec(T)"
grep "Triples Correction" *.out
echo "Etot"
grep "E(CCSD(T)" *.out

grep -B2 -A16 "FINAL SUMMARY DLPNO-CCSD ENERGY DECOMPOSITION (Eh)" *out
