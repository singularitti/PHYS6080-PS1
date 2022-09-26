export temperature

function temperature(particles)
    v² = map(particles) do particle
        sum(abs2, particle.v)
    end
    return 16 / length(particles) * sum(v²)
end

volume(particles) = length(particles) / ρ
